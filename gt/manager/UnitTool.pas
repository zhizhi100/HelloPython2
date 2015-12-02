unit UnitTool;

interface

uses Windows, Messages, Classes, SysUtils,WinSvc;

function GetServiceStatusString(sServiceName: string): string;
function StartService(AServName: string): Boolean; //use WinSvc
function StopService(AServName: string): Boolean;
function InstallService(AServName,log: string): Boolean;
function DeleteService(AServName,log: string): Boolean;
function RunDOS(const CommandLine: string): string;
function RunDosB(const CommandLine: string): string;
function RunDosCommand(Command: string): string;
function isrunning(serv:string):Boolean;
function stopserv(serv:string):Boolean;
function startserv(serv:string):Boolean;
function uninstallserv(serv:string):Boolean;
function installserv(serv,filename:string):Boolean;
function isinstalled(serv:string):Boolean;

implementation

function GetServiceStatusString(sServiceName: string): string;
var
  hService, hSCManager: SC_HANDLE;
  SS: TServiceStatus;
begin
  hSCManager := OpenSCManager(nil, SERVICES_ACTIVE_DATABASE, SC_MANAGER_CONNECT);
  if hSCManager = 0 then
  begin
    result := 'Can not open the service control manager';
    exit;
  end;
  hService := OpenService(hSCManager, PChar(sServiceName), SERVICE_QUERY_STATUS);
  if hService = 0 then
  begin
    CloseServiceHandle(hSCManager);
    result := 'Can not open the service(' + sServiceName + ')';
    exit;
  end;
  if not QueryServiceStatus(hService, SS) then
    result := 'Can not query the service status'
  else
  begin
    case SS.dwCurrentState of
      SERVICE_CONTINUE_PENDING:
        result := 'The service(' + sServiceName + ') continue is pending';
      SERVICE_PAUSE_PENDING:
        result := 'The service(' + sServiceName + ') pause is pending.';
      SERVICE_PAUSED:
        result := 'The service(' + sServiceName + ') is paused.';
      SERVICE_RUNNING:
        result := 'The service(' + sServiceName + ') is running.';
      SERVICE_START_PENDING:
        result := 'The service(' + sServiceName + ') is starting.';
      SERVICE_STOP_PENDING:
        result := 'The service(' + sServiceName + ') is stopping.';
      SERVICE_STOPPED:
        result := 'The service(' + sServiceName + ') is not running.';
    else
      result := 'Unknown Status';
    end;
  end;
  CloseServiceHandle(hSCManager);
  CloseServiceHandle(hService);
end;

function StartService(AServName: string): Boolean; //use WinSvc
var
  SCManager, hService: SC_HANDLE;
  lpServiceArgVectors: PChar;
begin
  SCManager := OpenSCManager(nil, nil, SC_MANAGER_ALL_ACCESS);
  Result := SCManager <> 0;
  if Result then
  try
    hService := OpenService(SCManager, PChar(AServName), SERVICE_ALL_ACCESS);
    Result := hService <> 0;
    if (hService = 0) and (GetLastError = ERROR_SERVICE_DOES_NOT_EXIST) then
      Exception.Create('The specified service does not exist');
    if hService <> 0 then
    try
      lpServiceArgVectors := nil;
      Result := WinSvc.StartService(hService, 0, PChar(lpServiceArgVectors));
      if not Result and (GetLastError = ERROR_SERVICE_ALREADY_RUNNING) then
        Result := True;
    finally
      CloseServiceHandle(hService);
    end;
  finally
    CloseServiceHandle(SCManager);
  end;
end;

//如果要轉載本文請注明出處,免的出現版權紛爭,我不喜歡看到那種轉載了我的作品卻不注明出處的人 Seven{See7di#Gmail.com}
function StopService(AServName: string): Boolean;
var
  SCManager, hService: SC_HANDLE;
  SvcStatus: TServiceStatus;
begin
  SCManager := OpenSCManager(nil, nil, SC_MANAGER_ALL_ACCESS);
  Result := SCManager <> 0;
  if Result then
  try
    hService := OpenService(SCManager, PChar(AServName), SERVICE_ALL_ACCESS);
    Result := hService <> 0;
    if Result then
    try //停止并卸载服务;
      Result := ControlService(hService, SERVICE_CONTROL_STOP, SvcStatus);
      //删除服务，这一句可以不要;
      // DeleteService(hService);
    finally
      CloseServiceHandle(hService);
    end;
  finally
    CloseServiceHandle(SCManager);
  end;
end;

function InstallService(AServName,log: string): Boolean;
begin
  WinExec(PAnsiChar(AServName+' --startup auto install >'+log),SW_HIDE);
end;

function DeleteService(AServName,log: string): Boolean;
begin
  WinExec(PAnsiChar(AServName+' remove >'+log),SW_HIDE);
end;

procedure CheckResult(b: Boolean);
begin
  if not b then
    raise Exception.Create(SysErrorMessage(GetLastError));
end;

function RunDOS(const CommandLine: string): string;
var
  HRead, HWrite: THandle;
  StartInfo: TStartupInfo;
  ProceInfo: TProcessInformation;
  b: Boolean;
  sa: TSecurityAttributes;
  inS: THandleStream;
  sRet: TStrings;
begin
  Result := '';
  FillChar(sa, sizeof(sa), 0);
//设置允许继承，否则在NT和2000下无法取得输出结果
  sa.nLength := sizeof(sa);
  sa.bInheritHandle := True;
  sa.lpSecurityDescriptor := nil;
  b := CreatePipe(HRead, HWrite, @sa, 0);
  CheckResult(b);

  FillChar(StartInfo, SizeOf(StartInfo), 0);
  StartInfo.cb := SizeOf(StartInfo);
  StartInfo.wShowWindow := SW_HIDE;
//使用指定的句柄作为标准输入输出的文件句柄,使用指定的显示方式
  StartInfo.dwFlags := STARTF_USESTDHANDLES or STARTF_USESHOWWINDOW;
  StartInfo.hStdError := HWrite;
  StartInfo.hStdInput := GetStdHandle(STD_INPUT_HANDLE); //HRead;
  StartInfo.hStdOutput := HWrite;

  b := CreateProcess(nil, //lpApplicationName: PChar 
    PChar(CommandLine), //lpCommandLine: PChar
    nil, //lpProcessAttributes: PSecurityAttributes
    nil, //lpThreadAttributes: PSecurityAttributes
    True, //bInheritHandles: BOOL
    CREATE_NEW_CONSOLE, nil, nil, StartInfo, ProceInfo);

  CheckResult(b);
  WaitForSingleObject(ProceInfo.hProcess, INFINITE);

  inS := THandleStream.Create(HRead);
  if inS.Size > 0 then
  begin
    sRet := TStringList.Create;
    sRet.LoadFromStream(inS);
    Result := sRet.Text;
    sRet.Free;
  end;
  inS.Free;

  CloseHandle(HRead);
  CloseHandle(HWrite);
end;

function RunDosB(const CommandLine: String): String;
var
  sa:TSecurityAttributes;   
  sd:  SECURITY_DESCRIPTOR;
  lpsa:  PSecurityAttributes;
  hReadPipe,hWritePipe :THandle;   
  si: TStartupInfo;
  pi: TProcessInformation ;
  dest: array [0..4095] of char;
  BytesRead: Dword;
  function IsWindowsNT: Boolean;   
  var
 osv: OSVERSIONINFO ;
  begin;
    osv.dwOSVersionInfoSize := sizeof(osv);
    GetVersionEx(osv);   
    if (osv.dwPlatformId = VER_PLATFORM_WIN32_NT) then
    Result :=TRUE ELSE rESULT:=False;
  end;
begin
  Result:='调用失败';
  lpsa := nil;   
  if (IsWindowsNT) then  
  begin
    InitializeSecurityDescriptor(@sd, SECURITY_DESCRIPTOR_REVISION);
    SetSecurityDescriptorDacl(@sd, true, nil, false);
    sa.nLength := sizeof(SECURITY_ATTRIBUTES);
    sa.bInheritHandle := true;
    sa.lpSecurityDescriptor := @sd;
    lpsa := @sa;
  end;   
  assert(CreatePipe(hReadPipe,hWritePipe,lpsa,2500000));
  GetStartupInfo(si);   
  si.cb := sizeof(TStartupInfo);   
  si.dwFlags := STARTF_USESHOWWINDOW + STARTF_USESTDHANDLES;
  si.wShowWindow := SW_HIDE;   
  si.hStdOutput := hWritePipe;   
  si.hStdError := hWritePipe;   
  CreateProcess(nil,PChar(CommandLine),nil,nil,TRUE,0,nil,nil,si,pi);   
  CloseHandle(pi.hThread);
  WaitForSingleObject(pi.hProcess, INFINITE);   
  if ReadFile(hReadPipe,dest,sizeof(dest),BytesRead,nil) then  
    Result:=Copy(String(dest),1,BytesRead);   
  CloseHandle(hReadPipe);   
  CloseHandle(hWritePipe);
  CloseHandle(pi.hProcess);
end;

function RunDosCommand(Command: string): string;
var
  hReadPipe: THandle;
  hWritePipe: THandle;
  SI: TStartUpInfo;
  PI: TProcessInformation;
  SA: TSecurityAttributes;
  //     SD   :   TSecurityDescriptor;
  BytesRead: DWORD;
  Dest: array[0..1023] of char;
  CmdLine: array[0..512] of char;
  TmpList: TStringList;
  Avail, ExitCode, wrResult: DWORD;
  osVer: TOSVERSIONINFO;
  tmpstr: AnsiString;
begin
  osVer.dwOSVersionInfoSize := Sizeof(TOSVERSIONINFO);
  GetVersionEX(osVer);
 
  if osVer.dwPlatformId = VER_PLATFORM_WIN32_NT then
  begin
  //         InitializeSecurityDescriptor(@SD,   SECURITY_DESCRIPTOR_REVISION);
  //         SetSecurityDescriptorDacl(@SD,   True,   nil,   False);
    SA.nLength := SizeOf(SA);
    SA.lpSecurityDescriptor := nil; //@SD;
    SA.bInheritHandle := True;
    CreatePipe(hReadPipe, hWritePipe, @SA, 0);
  end
  else
    CreatePipe(hReadPipe, hWritePipe, nil, 1024);
  try
    FillChar(SI, SizeOf(SI), 0);
    SI.cb := SizeOf(TStartUpInfo);
    SI.wShowWindow := SW_HIDE;
    SI.dwFlags := STARTF_USESHOWWINDOW;
    SI.dwFlags := SI.dwFlags or STARTF_USESTDHANDLES;
    SI.hStdOutput := hWritePipe;
    SI.hStdError := hWritePipe;
    StrPCopy(CmdLine, Command);
    if CreateProcess(nil, CmdLine, nil, nil, True, NORMAL_PRIORITY_CLASS, nil, nil, SI, PI) then
    begin
      ExitCode := 0;
      while ExitCode = 0 do
      begin
        wrResult := WaitForSingleObject(PI.hProcess, 500);
  //                 if   PeekNamedPipe(hReadPipe,   nil,   0,   nil,   @Avail,   nil)   then
        if PeekNamedPipe(hReadPipe, @Dest[0], 1024, @Avail, nil, nil) then
        begin
          if Avail > 0 then
          begin
            TmpList := TStringList.Create;
            try
              FillChar(Dest, SizeOf(Dest), 0);
              ReadFile(hReadPipe, Dest[0], Avail, BytesRead, nil);
              TmpStr := Copy(Dest, 0, BytesRead - 1);
              TmpList.Text := TmpStr;
              Result := tmpstr;
            finally
              TmpList.Free;
            end;
          end;
        end;
        if wrResult <> WAIT_TIMEOUT then ExitCode := 1;
      end;
      GetExitCodeProcess(PI.hProcess, ExitCode);
      CloseHandle(PI.hProcess);
      CloseHandle(PI.hThread);
    end;
  finally
    CloseHandle(hReadPipe);
    CloseHandle(hWritePipe);
  end;
end;

function phrease_serv_state(s:string):Integer;
var
  i : Integer;
begin
  i := Pos('STATE',s);
  if (i = 0) then
  begin
    Result := 0;
    Exit;
  end
  else
  begin
    Result := 100;
    i := Pos('STOPPED',s);
    if ( i > 0 ) then
    begin
      Result := 1;
      Exit;
    end;
    i := Pos('START_PENDING',s);
    if ( i > 0 ) then
    begin
      Result := 2;
      Exit;
    end;
    i := Pos('STOP_PENDING',s);
    if ( i > 0 ) then
    begin
      Result := 3;
      Exit;
    end;
    i := Pos('RUNNING',s);
    if ( i > 0 ) then
    begin
      Result := 4;
      Exit;
    end;
  end;
end;

function installserv(serv,filename:string):Boolean;
var
  cmd,ret:string;
  k : Integer;
begin
  if not FileExists(filename) then
  begin
    Result := False;
    Exit;
  end
  else
  begin
    cmd := 'sc create '+serv+ '  start= auto binPath= '+filename;
    ret := RunDosCommand(cmd);
    Sleep(500);
    cmd := 'sc query '+serv;
    ret := RunDosCommand(cmd);
    k := phrease_serv_state(ret);
    if (k > 0) then
    begin
      Result := True;
    end
    else
    begin
      Result := False;
    end;
  end;              
end;

function uninstallserv(serv:string):Boolean;
var
  cmd,ret:string;
  k : Integer;
begin
  cmd := 'sc stop '+serv;
  ret := RunDosCommand(cmd);
  Sleep(200);
  cmd := 'sc delete '+serv;
  ret := RunDosCommand(cmd);
  Sleep(200);
  cmd := 'sc query '+serv;
  ret := RunDosCommand(cmd);
  k := phrease_serv_state(ret);
  if ( k > 0) then
  begin
    Result := False;
  end
  else
  begin
    Result := True;
  end;
end;

function startserv(serv:string):Boolean;
var
  cmd,ret:string;
  k : Integer;
begin
  cmd := 'sc start '+serv;
  ret := RunDosCommand(cmd);
  Sleep(200);
  cmd := 'sc query '+serv;
  ret := RunDosCommand(cmd);
  k := phrease_serv_state(ret);
  if ( k = 2) or (k = 4) then
  begin
    Result := True;
  end
  else
  begin
    Result := False;
  end;
end;

function stopserv(serv:string):Boolean;
var
  cmd,ret:string;
  k : Integer;
begin
  cmd := 'sc stop '+serv;
  ret := RunDosCommand(cmd);
  Sleep(200);
  cmd := 'sc query '+serv;
  ret := RunDosCommand(cmd);
  k := phrease_serv_state(ret);
  if ( k = 2) or (k = 4) then
  begin
    Result := False;
  end
  else
  begin
    Result := True;
  end;
end;

function isrunning(serv:string):Boolean;
var
  cmd,ret:string;
  k : Integer;
begin
  cmd := 'sc query '+serv;
  ret := RunDosCommand(cmd);
  k := phrease_serv_state(ret);
  if ( k = 4) then
  begin
    Result := True;
  end
  else
  begin
    Result := False;
  end;
end;

function isinstalled(serv:string):Boolean;
var
  cmd,ret:string;
  k : Integer;
begin
  cmd := 'sc query '+serv;
  ret := RunDosCommand(cmd);
  k := phrease_serv_state(ret);
  if ( k > 0) then
  begin
    Result := True;
  end
  else
  begin
    Result := False;
  end;
end;

end.

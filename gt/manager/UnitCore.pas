unit UnitCore;

interface

uses
  Windows, Messages, Classes, SysUtils, WinSvc, IniFiles, MD5, Shellapi,
  Controls, Dialogs, Forms, Winsock, ComObj, ActiveX, ShlObj, Registry;

function checkKey(): string;

procedure quicklink();

implementation

type
  TIPList = array of string;

function SplitString(const source, ch: string): TStringList;
var
  temp, t2: string;
  i: integer;
begin
  result := TStringList.Create;
  temp := source;
  i := pos(ch, source);
  while i <> 0 do
  begin
    t2 := copy(temp, 0, i - 1);
    if (t2 <> '') then
      result.Add(t2);
    delete(temp, 1, i - 1 + Length(ch));
    i := pos(ch, temp);
  end;
  result.Add(temp);
end;

function getIP: TIPList;
type
  TaPInAddr = array[0..10] of PInAddr;

  PaPInAddr = ^TaPInAddr;
const
  BufferSize = 64;
var
  phe: PHostEnt;
  pptr: PaPInAddr;
  Buffer: PAnsiChar;
  I: Integer;
  GInitData: TWSADATA;
begin
  WSAStartup($101, GInitData);
  getMem(Buffer, BufferSize);
  GetHostName(Buffer, BufferSize);
  phe := GetHostByName(buffer);
  if phe = nil then
    Exit;
  pptr := PaPInAddr(Phe^.h_addr_list);
  I := 0;
  while pptr^[I] <> nil do
  begin
    Inc(I);
  end;
  setLength(result, I);
  for I := low(result) to high(result) do
    result[i] := StrPas(inet_ntoa(pptr^[I]^));
  freeMem(Buffer);
  WSACleanup;
end;

//-----------------------------------------------
//16进制字符转整数,16进制字符与字符串转换中间函数
//-----------------------------------------------
function HexToInt(hex: string): integer;
var
  i: integer;

  function Ncf(num, f: integer): integer;
  var
    i: integer;
  begin
    Result := 1;
    if f = 0 then
      exit;
    for i := 1 to f do
      result := result * num;
  end;

  function HexCharToInt(HexToken: char): integer;
  begin
    if HexToken > #97 then
      HexToken := Chr(Ord(HexToken) - 32);
    Result := 0;
    if (HexToken > #47) and (HexToken < #58) then { chars 0....9 }
      Result := Ord(HexToken) - 48
    else if (HexToken > #64) and (HexToken < #71) then { chars A....F }
      Result := Ord(HexToken) - 65 + 10;
  end;

begin
  result := 0;
  hex := ansiuppercase(trim(hex));
  if hex = '' then
    exit;
  for i := 1 to length(hex) do
    result := result + HexCharToInt(hex[i]) * ncf(16, length(hex) - i);
end;
 
 
 
//-----------------------------------------------
//字符串转16进制字符
//-----------------------------------------------
function StringToHex(str: string): string;
var
  i: integer;
  s: string;
begin
  for i := 1 to length(str) do
  begin
    s := s + InttoHex(Integer(str[i]), 2);
  end;
  Result := s;
end;
 
 
 
//-----------------------------------------------
//16进制字符转字符串 
//-----------------------------------------------
function hextostring(str: string): string;
var
  s, t: string;
  i, j: integer;
  p: pchar;
begin
  s := '';
  i := 1;
  while i < length(str) do
  begin
    t := str[i] + str[i + 1];
    s := s + chr(hextoint(t));
    i := i + 2;
  end;
  result := s;
end;

function checkKey(): string;
var
  _eax, _ebx, _ecx, _edx: Longword;
  s, s1, s2, results, feature: string;
  md5: TMD5Digest;
  t: string;
  p: string;
  fn: string;
  key, key1, key2: string;
  F: TextFile;
  days: Integer;
  a: TDateTime;
  FSetting: TFormatSettings;
  valid: Boolean;
  ips: TIPList;
  ipstr: string;
  ip: TStringList;
  i: Integer;
begin
  p := ExtractFileDir(Application.Exename);
  Result := '您尚未申请试用授权';
  ips := getIP();
  i := low(ips);
  ipstr := ips[i];
  if FileExists(p + '\' + ipstr + '.lic') then
  begin
    Result := '存在正式授权！';
    Exit;
  end;
  ip := SplitString(ipstr, '.');
  ipstr := IntToHex(StrToInt(ip[0]) + 255, 0) + IntToHex(StrToInt(ip[1]) + 255, 0) + IntToHex(StrToInt(ip[2]) + 255, 0) + IntToHex(StrToInt(ip[3]) + 255, 0);
  asm
        push    eax
        push    ebx
        push    ecx
        push    edx
        mov     eax, 1
        db      $0F, $A2
        mov     _eax, eax
        mov     _ebx, ebx
        mov     _ecx, ecx
        mov     _edx, edx
        pop     edx
        pop     ecx
        pop     ebx
        pop     eax
  end;
  s := IntToHex(_eax, 8);
  s1 := IntToHex(_edx, 8);
  s2 := IntToHex(_ecx, 8);
  results := s1 + s;
  t := s1 + s;
  feature := t;
  MD5String(t, @md5);
  feature := MD5DigestToStr(md5);
  t := feature;

  fn := p + '\key.triallic';
  if not FileExists(fn) then
    Exit;
  AssignFile(F, fn); { File selected in dialog }
  Reset(F);
  Readln(F, S);                        { Read first line of file }
  key := s;
  CloseFile(F);
  if Length(key) > 5 then
  begin
    key1 := copy(key, 0, 4);
    key2 := Copy(key, 5, 3);
    days := HexToInt(key2);
    days := days mod 1000;
      //FSetting := TFormatSettings.Create(LOCALE_USER_DEFAULT);
    FSetting.ShortDateFormat := 'yyyy-MM-dd';
    FSetting.DateSeparator := '-';
      //FSetting.TimeSeparator:=':';
    FSetting.LongTimeFormat := 'hh:mm:ss.zzz';
    a := StrToDateTime('2015-01-01 00:00:00.000', FSetting);
    a := a + days;
    s := FormatDateTime('yyyymmdd', a);
    s := t + s;
    MD5String(s, @md5);
    t := MD5DigestToStr(md5);
    s := '' + t[1] + t[9] + t[17] + t[25];
    if (key1 = s) then
    begin
       //显示授权内容
      valid := True;
      Result := '试用期限：' + FormatDateTime('yyyy-mm-dd', a);
    end;
  end;
end;

procedure CreateLink(ProgramPath, ProgramArg, LinkPath, Descr: string);
var
  AnObj: IUnknown;
  ShellLink: IShellLink;
  AFile: IPersistFile;
  FileName: WideString;
begin
  if UpperCase(ExtractFileExt(LinkPath)) <> '.LNK' then //检查扩展名是否正确
  begin
    raise Exception.Create('快捷方式的扩展名必须是 "LNK"!'); //若不是则产生异常
  end;
  try
    OleInitialize(nil); //初始化OLE库，在使用OLE函数前必须调用初始化
    AnObj := CreateComObject(CLSID_ShellLink); //根据给定的ClassID生成一个COM对象，此处是快捷方式
    ShellLink := AnObj as IShellLink; //强制转换为快捷方式接口
    AFile := AnObj as IPersistFile; //强制转换为文件接口 
//设置快捷方式属性，此处只设置了几个常用的属性
    ShellLink.SetPath(PChar(ProgramPath)); // 快捷方式的目标文件，一般为可执行文件
    ShellLink.SetArguments(PChar(ProgramArg)); // 目标文件参数
    ShellLink.SetWorkingDirectory(PChar(ExtractFilePath(ProgramPath))); //目标文件的工作目录
    ShellLink.SetDescription(PChar(Descr)); // 对目标文件的描述
    FileName := LinkPath; //把文件名转换为WideString类型
    AFile.Save(PWChar(FileName), False); //保存快捷方式
  finally
    OleUninitialize; //关闭OLE库，此函数必须与OleInitialize成对调用
  end;
end;

function GetShellFolders(strDir: string): string;
const
  regPath = '\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders';
var
  Reg: TRegistry;
  strFolders: string;
begin
  Reg := TRegistry.Create;
  try
    Reg.RootKey := HKEY_CURRENT_USER;
    if Reg.OpenKey(regPath, false) then begin
      strFolders := Reg.ReadString(strDir);
    end;
  finally
    Reg.Free;
  end;
  result := strFolders;
end;
      
{获取桌面}
      
function GetDeskeptPath: string;
begin
  Result := GetShellFolders('Desktop'); //是取得桌面文件夹的路径
end;
      
{获取我的文档}
      
function GetMyDoumentpath: string;
begin
  Result := GetShellFolders('Personal'); //我的文档
end;

procedure quicklink();
var
  tmpObject: IUnknown;
  tmpSLink: IShellLink;
  tmpPFile: IPersistFile;
  PIDL: PItemIDList;
  StartupDirectory: array[0..MAX_PATH] of Char;
  StartupFilename: string;
  LinkFilename: WideString;
begin
//创建快捷方式到桌面
  StartupFilename := Application.ExeName;
  tmpObject := CreateComObject(CLSID_ShellLink); //创建建立快捷方式的外壳扩展
  tmpSLink := tmpObject as IShellLink; //取得接口
  tmpPFile := tmpObject as IPersistFile; //用来储存*.lnk文件的接口
  tmpSLink.SetPath(pChar(StartupFilename)); //设定所在路径
  tmpSLink.SetWorkingDirectory(pChar(ExtractFilePath(StartupFilename))); //设定工作目录
  SHGetSpecialFolderLocation(0, CSIDL_DESKTOPDIRECTORY, PIDL); //获得桌面的Itemidlist
  tmpSLink.SetDescription('金三助手管理工具');
  tmpSLink.SetIconLocation(Pchar(StartupFilename), 0);
  SHGetPathFromIDList(PIDL, StartupDirectory); //获得桌面路径
  LinkFilename := StartupDirectory + '\金三助手管理.lnk';
  tmpPFile.Save(pWChar(LinkFilename), FALSE); //保存*.lnk文
end;

end.


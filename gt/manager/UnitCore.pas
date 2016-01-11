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
//16�����ַ�ת����,16�����ַ����ַ���ת���м亯��
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
//�ַ���ת16�����ַ�
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
//16�����ַ�ת�ַ��� 
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
  Result := '����δ����������Ȩ';
  ips := getIP();
  i := low(ips);
  ipstr := ips[i];
  if FileExists(p + '\' + ipstr + '.lic') then
  begin
    Result := '������ʽ��Ȩ��';
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
       //��ʾ��Ȩ����
      valid := True;
      Result := '�������ޣ�' + FormatDateTime('yyyy-mm-dd', a);
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
  if UpperCase(ExtractFileExt(LinkPath)) <> '.LNK' then //�����չ���Ƿ���ȷ
  begin
    raise Exception.Create('��ݷ�ʽ����չ�������� "LNK"!'); //������������쳣
  end;
  try
    OleInitialize(nil); //��ʼ��OLE�⣬��ʹ��OLE����ǰ������ó�ʼ��
    AnObj := CreateComObject(CLSID_ShellLink); //���ݸ�����ClassID����һ��COM���󣬴˴��ǿ�ݷ�ʽ
    ShellLink := AnObj as IShellLink; //ǿ��ת��Ϊ��ݷ�ʽ�ӿ�
    AFile := AnObj as IPersistFile; //ǿ��ת��Ϊ�ļ��ӿ� 
//���ÿ�ݷ�ʽ���ԣ��˴�ֻ�����˼������õ�����
    ShellLink.SetPath(PChar(ProgramPath)); // ��ݷ�ʽ��Ŀ���ļ���һ��Ϊ��ִ���ļ�
    ShellLink.SetArguments(PChar(ProgramArg)); // Ŀ���ļ�����
    ShellLink.SetWorkingDirectory(PChar(ExtractFilePath(ProgramPath))); //Ŀ���ļ��Ĺ���Ŀ¼
    ShellLink.SetDescription(PChar(Descr)); // ��Ŀ���ļ�������
    FileName := LinkPath; //���ļ���ת��ΪWideString����
    AFile.Save(PWChar(FileName), False); //�����ݷ�ʽ
  finally
    OleUninitialize; //�ر�OLE�⣬�˺���������OleInitialize�ɶԵ���
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
      
{��ȡ����}
      
function GetDeskeptPath: string;
begin
  Result := GetShellFolders('Desktop'); //��ȡ�������ļ��е�·��
end;
      
{��ȡ�ҵ��ĵ�}
      
function GetMyDoumentpath: string;
begin
  Result := GetShellFolders('Personal'); //�ҵ��ĵ�
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
//������ݷ�ʽ������
  StartupFilename := Application.ExeName;
  tmpObject := CreateComObject(CLSID_ShellLink); //����������ݷ�ʽ�������չ
  tmpSLink := tmpObject as IShellLink; //ȡ�ýӿ�
  tmpPFile := tmpObject as IPersistFile; //��������*.lnk�ļ��Ľӿ�
  tmpSLink.SetPath(pChar(StartupFilename)); //�趨����·��
  tmpSLink.SetWorkingDirectory(pChar(ExtractFilePath(StartupFilename))); //�趨����Ŀ¼
  SHGetSpecialFolderLocation(0, CSIDL_DESKTOPDIRECTORY, PIDL); //��������Itemidlist
  tmpSLink.SetDescription('�������ֹ�����');
  tmpSLink.SetIconLocation(Pchar(StartupFilename), 0);
  SHGetPathFromIDList(PIDL, StartupDirectory); //�������·��
  LinkFilename := StartupDirectory + '\�������ֹ���.lnk';
  tmpPFile.Save(pWChar(LinkFilename), FALSE); //����*.lnk��
end;

end.


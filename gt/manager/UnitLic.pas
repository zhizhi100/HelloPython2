unit UnitLic;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, ExtCtrls, md5, shellapi;

type
  Tfrmlic = class(TForm)
    lbl1: TLabel;
    edtfeature: TEdit;
    Label1: TLabel;
    edtkey: TEdit;
    btngetkey: TButton;
    btn1: TButton;
    lbl2: TLabel;
    btn2: TButton;
    pnl1: TPanel;
    procedure FormShow(Sender: TObject);
    procedure btngetkeyClick(Sender: TObject);
    procedure btn2Click(Sender: TObject);
    procedure btn3Click(Sender: TObject);
  private
    { Private declarations }
    feature : string;
  public
    { Public declarations }
  end;

var
  frmlic: Tfrmlic;

implementation

{$R *.dfm}

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
    if f = 0 then exit;
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
   i : integer;
   s : string;
begin
   for i:=1 to length(str) do begin
       s := s + InttoHex(Integer(str[i]),2);
   end;
   Result:=s;
end;
 
 
 
//-----------------------------------------------
//16进制字符转字符串 
//-----------------------------------------------
function hextostring(str: string): string;
var
  s,t:string;
  i,j:integer;
  p:pchar;
begin
   s:='';
   i:=1;
   while i< length(str) do begin
      t:=str[i]+str[i+1];
      s:=s+chr(hextoint(t));
      i:=i+2;
   end;
   result:=s;
end;

procedure Tfrmlic.FormShow(Sender: TObject);
var
   _eax, _ebx, _ecx, _edx: Longword;
   s, s1, s2,result: string;
   md5: TMD5Digest;
   t : string;
begin
  asm
     push eax
     push ebx
     push ecx
     push edx
     mov eax,1
     db $0F,$A2
     mov _eax,eax
     mov _ebx,ebx
     mov _ecx,ecx
     mov _edx,edx
     pop edx
     pop ecx
     pop ebx
     pop eax
    end;
   s := IntToHex(_eax, 8);
   s1 := IntToHex(_edx, 8);
   s2 := IntToHex(_ecx, 8);
   //result:=s+'|'+s1+'|'+s2;
   result := s1+s;
   //edtfeature.Text := s1 + s;
   t := s1 + s;
   feature := t;
   MD5String(t,@md5);
   //edit1.Text:=MD5DigestToStr(md5);
   edtfeature.Text := MD5DigestToStr(md5);
end;

procedure Tfrmlic.btngetkeyClick(Sender: TObject);
var
  url : string;
begin
  url := 'http://127.0.0.1:8001/trial.html?id='+feature;
  ShellExecute(Handle, 'open', 'IExplore.EXE', PChar(url), nil, SW_SHOWNORMAL);
end;

procedure Tfrmlic.btn2Click(Sender: TObject);
var
   _eax, _ebx, _ecx, _edx: Longword;
   s, s1, s2,result: string;
   md5: TMD5Digest;
   t : string;
   crc : string;
   key,key1,key2:string;
   days : Integer;
   a:TDateTime;
   p : string;
   f : string;
   FileHandle : Integer;
   F1 : TextFile;
   FSetting : TFormatSettings;
   valid : Boolean;
begin
  valid := False;
  asm
     push eax
     push ebx
     push ecx
     push edx
     mov eax,1
     db $0F,$A2
     mov _eax,eax
     mov _ebx,ebx
     mov _ecx,ecx
     mov _edx,edx
     pop edx
     pop ecx
     pop ebx
     pop eax
    end;
   s := IntToHex(_eax, 8);
   s1 := IntToHex(_edx, 8);
   s2 := IntToHex(_ecx, 8);
   //result:=s+'|'+s1+'|'+s2;
   result := s1+s;
   //edtfeature.Text := s1 + s;
   t := s1 + s;
   MD5String(t,@md5);
   t := MD5DigestToStr(md5);
   key := edtkey.Text;
   if Length(key) > 5 then
   begin
     key1 := copy(key,0,4);
     key2 := Copy(key,5,3);
     days := HexToInt(key2);
     days := days mod 1000;
      //FSetting := TFormatSettings.Create(LOCALE_USER_DEFAULT);
      FSetting.ShortDateFormat:='yyyy-MM-dd';
      FSetting.DateSeparator:='-';
      //FSetting.TimeSeparator:=':';
      FSetting.LongTimeFormat:='hh:mm:ss.zzz';
     a:=StrToDateTime('2015-01-01 00:00:00.000', FSetting);
     a := a + days;
     s := FormatDateTime('yyyymmdd',a);
     s := t + s;
     MD5String(s,@md5);
     t := MD5DigestToStr(md5);
     s := '' + t[1] + t[9] + t[17] + t[25];
     if (key1 = s) then
     begin
       p := ExtractFileDir(Application.Exename);
       f := p + '\key.triallic';
       if not(FileExists(f)) then
       begin
         FileHandle := FileCreate(f);
         FileClose(FileHandle);
       end;
       AssignFile(F1,f);
       Rewrite(F1);
       write(f1,key);
       CloseFile(f1);
       //显示授权内容
       valid := True;
       pnl1.Caption := '试用期限：'+ FormatDateTime('yyyy-mm-dd',a);
     end;
   end;
   if not valid then
   begin
     ShowMessage('您输入的试用密钥不可用！');
   end;
end;

procedure Tfrmlic.btn3Click(Sender: TObject);
var
  id : string;
  d:Integer;
  a:TDateTime;
  s,key1,key2,key:string;
  md5: TMD5Digest;
  FSetting : TFormatSettings;
begin
  //FSetting := TFormatSettings.Create(LOCALE_USER_DEFAULT);
  FSetting.ShortDateFormat:='yyyy-MM-dd';
  FSetting.DateSeparator:='-';
  //FSetting.TimeSeparator:=':';
  FSetting.LongTimeFormat:='hh:mm:ss.zzz';
  id := '554EDC5A89BCE95177CBCAB199BFBA5C';
  d := 30;
  key2 := IntToHex(30 + 1000,0);
  a:=StrToDateTime('2015-01-01 00:00:00.000', FSetting);
  a := a + d;
  s := FormatDateTime('yyyymmdd',a);
  s := id + s;
  MD5String(s,@md5);
  s := MD5DigestToStr(md5);
  key1 := '' + s[1] + s[9] + s[17] + s[25];
  key := key1 + key2;
  edtkey.Text := key;
end;

end.

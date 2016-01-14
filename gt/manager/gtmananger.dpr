program gtmananger;

uses
  Forms,
  Windows,
  Dialogs,
  System,
  SysUtils,
  UnitMain in 'UnitMain.pas' {FormMain},
  UnitAbout in 'UnitAbout.pas' {AboutBox},
  UnitTool in 'UnitTool.pas',
  UnitTest in 'UnitTest.pas' {frmtest},
  GetDSN in 'GetDSN.pas',
  UnitLic in 'UnitLic.pas' {frmlic},
  UnitAuto in 'UnitAuto.pas' {frminstall},
  UnitCore in 'UnitCore.pas',
  util_utf8 in 'util_utf8.pas',
  uQRCode in 'uQRCode.pas',
  bitstream in 'qrcode\bitstream.pas',
  mask in 'qrcode\mask.pas',
  mmask in 'qrcode\mmask.pas',
  mqrspec in 'qrcode\mqrspec.pas',
  qrenc in 'qrcode\qrenc.pas',
  qrencode in 'qrcode\qrencode.pas',
  qrinput in 'qrcode\qrinput.pas',
  qrspec in 'qrcode\qrspec.pas',
  rscode in 'qrcode\rscode.pas',
  split in 'qrcode\split.pas',
  struct in 'qrcode\struct.pas';

{$R *.res}
var 
  mymutex: THandle;
  A: Hwnd;
begin
  mymutex:=CreateMutex(nil,True,'�ҵĻ������'); 
  if GetLastError=ERROR_ALREADY_EXISTS then
  begin
    //A := FindWindow(nil,'�������ֹ����� Golden Manager');
    //if A <> 0 then ShowWindow(A,SW_SHowNormal);
    showmessage('���Ѿ������������ֹ�����');
    closeHandle(mymutex);
    Exit;
  end;
  Application.Initialize;
  Application.CreateForm(TFormMain, FormMain);
  Application.CreateForm(TAboutBox, AboutBox);
  Application.CreateForm(Tfrmtest, frmtest);
  Application.CreateForm(Tfrmlic, frmlic);
  Application.CreateForm(Tfrminstall, frminstall);
  Application.Run;
  ReleaseMutex(mymutex);
end.

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
  uQRCode in 'uQRCode.pas';

{$R *.res}
var 
  mymutex: THandle;
  A: Hwnd;
begin
  mymutex:=CreateMutex(nil,True,'我的互斥对象'); 
  if GetLastError=ERROR_ALREADY_EXISTS then
  begin
    //A := FindWindow(nil,'金三助手管理工具 Golden Manager');
    //if A <> 0 then ShowWindow(A,SW_SHowNormal);
    showmessage('您已经启动金三助手管理工具');
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

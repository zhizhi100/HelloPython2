program gtmananger;

uses
  Forms,
  UnitMain in 'UnitMain.pas' {FormMain},
  UnitAbout in 'UnitAbout.pas' {AboutBox},
  UnitTool in 'UnitTool.pas',
  UnitTest in 'UnitTest.pas' {frmtest},
  GetDSN in 'GetDSN.pas',
  UnitLic in 'UnitLic.pas' {frmlic};

{$R *.res}

begin
  Application.Initialize;
  Application.CreateForm(TFormMain, FormMain);
  Application.CreateForm(TAboutBox, AboutBox);
  Application.CreateForm(Tfrmtest, frmtest);
  Application.CreateForm(Tfrmlic, frmlic);
  Application.Run;
end.

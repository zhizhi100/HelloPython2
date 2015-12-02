unit UnitTest;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, Menus, UnitTool, StdCtrls, ExtCtrls, IniFiles;

type
  Tfrmtest = class(TForm)
    mm1: TMainMenu;
    N1: TMenuItem;
    N2: TMenuItem;
    N3: TMenuItem;
    N4: TMenuItem;
    N5: TMenuItem;
    N6: TMenuItem;
    cmd1: TMenuItem;
    lbledtcmd: TLabeledEdit;
    N7: TMenuItem;
    ini1: TMenuItem;
    procedure N2Click(Sender: TObject);
    procedure cmd1Click(Sender: TObject);
    procedure N3Click(Sender: TObject);
    procedure N4Click(Sender: TObject);
    procedure N5Click(Sender: TObject);
    procedure N6Click(Sender: TObject);
    procedure ini1Click(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frmtest: Tfrmtest;

implementation

{$R *.dfm}

procedure Tfrmtest.N2Click(Sender: TObject);
var
  i : Boolean;
begin
  i := installserv('ServA','E:\test\gtmanager\serva.exe');
  if i then
    ShowMessage('yes')
  else
    ShowMessage('oh!no!');
end;

procedure Tfrmtest.cmd1Click(Sender: TObject);
var
  cmd : string;
begin
  cmd := 'sc create ServA binPath= E:\test\gtmanager\serva.exe';
  cmd := lbledtcmd.Text;
  ShowMessage(RunDosCommand(cmd));
end;

procedure Tfrmtest.N3Click(Sender: TObject);
var
  i : Boolean;
begin
  i := uninstallserv('ServA');
  if i then
    ShowMessage('yes')
  else
    ShowMessage('oh!no!');
end;

procedure Tfrmtest.N4Click(Sender: TObject);
var
  i : Boolean;
begin
  i := isrunning('ServA');
  if i then
    ShowMessage('yes')
  else
    ShowMessage('oh!no!');
end;

procedure Tfrmtest.N5Click(Sender: TObject);
var
  i : Boolean;
begin
  i := startserv('ServA');
  if i then
    ShowMessage('yes')
  else
    ShowMessage('oh!no!');
end;

procedure Tfrmtest.N6Click(Sender: TObject);
var
  i : Boolean;
begin
  i := stopserv('ServA');
  if i then
    ShowMessage('yes')
  else
    ShowMessage('oh!no!');
end;

procedure Tfrmtest.ini1Click(Sender: TObject);
var
  MyIniFile: TIniFile;
  p : string;
begin
  p := ExtractFileDir(Application.Exename);
  MyIniFile := TIniFile.Create(p+'\myapp.ini');
  MyIniFile.WriteString('Transfer', 'Title1', 'Picture Painter');
  MyIniFile.Free;
end;

end.

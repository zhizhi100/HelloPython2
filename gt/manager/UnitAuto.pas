unit UnitAuto;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, UnitCore, UnitTool, Registry, Shellapi, IniFiles;

type
  Tfrminstall = class(TForm)
    lbl1: TLabel;
    grp1: TGroupBox;
    btnok: TButton;
    btnyes: TButton;
    chkquick: TCheckBox;
    chkreg: TCheckBox;
    chkstart: TCheckBox;
    chkieproxy: TCheckBox;
    lbl2: TLabel;
    chklocal: TCheckBox;
    chkproxy: TCheckBox;
    procedure btnokClick(Sender: TObject);
    procedure btnyesClick(Sender: TObject);
  private
    { Private declarations }
  public
    { Public declarations }
  end;

var
  frminstall: Tfrminstall;

implementation

{$R *.dfm}

procedure Tfrminstall.btnokClick(Sender: TObject);
begin
  Close();
end;

procedure Tfrminstall.btnyesClick(Sender: TObject);
var
  path : string;
  ARegistry : TRegistry;
  url : string;
  a,b:Boolean;
  p,fa,fb : string;
  iniFile:TiniFile;
  proxyserv,webserv : string;
begin
  if chkquick.Checked then
  begin
    quicklink();
  end;

  if chkieproxy.Checked then
  begin
    path := 'file://'+ExtractFilePath(Application.Exename)+'static/gtproxy.pac';
    ARegistry := TRegistry.Create; //建立一个TRegistry实例
    with ARegistry do
    begin
      RootKey := HKEY_CURRENT_USER;
      if OpenKey('Software\Microsoft\Windows\CurrentVersion\Internet Settings', True) then
      begin
        WriteString('AutoConfigURL', path);
      end;
      CloseKey;
      Destroy;
    end;
  end;

  p := ExtractFileDir(Application.Exename)+'\service.ini';
  iniFile := TiniFile.Create(p);
  proxyserv := iniFile.ReadString('service','proxy','proxy');
  webserv := iniFile.ReadString('service','local','local');
  inifile.free();

  if chkreg.Checked then
  begin
    p := ExtractFileDir(Application.Exename);
    fa := p + '/' + proxyserv + '.exe';
    fb := p + '/' + webserv + '.exe';
    a := installserv(proxyserv,fa);
    b := installserv(webserv,fb);
  end;

  if chkstart.Checked then
  begin
    a := startserv(proxyserv);
    b := startserv(webserv);
  end;

  if chklocal.Checked then
  begin
    url := 'http://127.0.0.1:8001/static/LocalServer.html';
    ShellExecute(Handle, 'open', 'IExplore.EXE', PChar(url), nil, SW_SHOWNORMAL);
  end;

  if chkproxy.Checked then
  begin
    url := 'http://www.google.com/_gtool_/GoldenToolProxy.html';
    ShellExecute(Handle, 'open', 'IExplore.EXE', PChar(url), nil, SW_SHOWNORMAL);
  end;
  close();
end;

end.

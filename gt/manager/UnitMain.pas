unit UnitMain;

interface

uses
  Windows, Messages, SysUtils, Variants, Classes, Graphics, Controls, Forms,
  Dialogs, StdCtrls, Buttons, Menus, UnitAbout, IniFiles, UnitTool, 
  ExtCtrls, shellapi, DateUtils, UnitLic, Registry;

type
  TFormMain = class(TForm)
    GroupBox1: TGroupBox;
    Label1: TLabel;
    Label2: TLabel;
    lblproxy: TLabel;
    lblweb: TLabel;
    GroupBox2: TGroupBox;
    btnstrart: TButton;
    btnstop: TButton;
    btnrestart: TButton;
    GroupBox3: TGroupBox;
    GroupBox4: TGroupBox;
    btninstall: TButton;
    btnremove: TButton;
    btnmore: TBitBtn;
    chkagree: TCheckBox;
    rbtmp: TRadioButton;
    rbproxy: TRadioButton;
    rbweb: TRadioButton;
    mmolog: TMemo;
    pm1: TPopupMenu;
    N1: TMenuItem;
    lbl1: TLabel;
    test1: TMenuItem;
    N2: TMenuItem;
    N3: TMenuItem;
    N4: TMenuItem;
    N5: TMenuItem;
    N6: TMenuItem;
    N7: TMenuItem;
    tmr1: TTimer;
    N8: TMenuItem;
    N9: TMenuItem;
    N10: TMenuItem;
    IE1: TMenuItem;
    N11: TMenuItem;
    procedure btnmoreClick(Sender: TObject);
    procedure N1Click(Sender: TObject);
    procedure N2Click(Sender: TObject);
    procedure N3Click(Sender: TObject);
    procedure FormShow(Sender: TObject);
    procedure N7Click(Sender: TObject);
    procedure btninstallClick(Sender: TObject);
    procedure tmr1Timer(Sender: TObject);
    procedure btnremoveClick(Sender: TObject);
    procedure btnstrartClick(Sender: TObject);
    procedure btnstopClick(Sender: TObject);
    procedure lbl1Click(Sender: TObject);
    procedure N8Click(Sender: TObject);
    procedure N9Click(Sender: TObject);
    procedure chkagreeMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure N11Click(Sender: TObject);
    procedure rbtmpMouseUp(Sender: TObject; Button: TMouseButton;
      Shift: TShiftState; X, Y: Integer);
    procedure IE1Click(Sender: TObject);
  private
    { Private declarations }
    proxyserv : string;
    webserv : string;
    proxylog : string;
    weblog : string;
    tmplog : string;
    registed : Boolean;
    procedure readini();
    procedure showregisted();
    procedure showunregisted();
    procedure showrunning();
    procedure showstopped();
    function queryservice(serv : string):Boolean;
    function isregisted():Boolean;
    procedure querystate();
    procedure queryinstalnation();
  public
    { Public declarations }
  end;

var
  FormMain: TFormMain;

implementation

{$R *.dfm}
function readlog(f:string):string;
var
  iFileHandle: Integer;
  Buffer: PChar;
  i : Integer;
  size: Integer;
begin
  size := 4096;
  Result := '';
  if FileExists(f) then
  begin
    try
      iFileHandle := FileOpen(f, fmShareDenyNone);
      i := FileSeek(iFileHandle, (0- size), 2);
      Buffer := PChar(AllocMem(size + 1));
      i := FileRead(iFileHandle, Buffer^, size);
      FileClose(iFileHandle);
      Result := strPas(Buffer);
    finally
      FreeMem(Buffer);
    end;
  end;
end;

procedure TFormMain.queryinstalnation();
var
  a,b:Boolean;
begin
  a := isinstalled(proxyserv);
  b := isinstalled(webserv);
  if a and b then
  begin
    showregisted();
  end
  else
  begin
    showunregisted();
  end;
end;

procedure TFormMain.querystate();
var
  a, b: Boolean;
begin
  a := isrunning(proxyserv);
  b := isrunning(webserv);
  if a and b then
  begin
    showrunning;
  end
  else
  begin
    showstopped;
    if a then
      lblproxy.Font.Color := clGreen;
    if b then
      lblweb.Font.Color := clGreen;
  end;
end;

function TFormMain.isregisted():Boolean;
var
  a,b:Boolean;
begin
  a := isinstalled(proxyserv);
  b := isinstalled(webserv);
  registed := a and b;
  Result := a and b;
end;

function TFormMain.queryservice(serv : string):Boolean;
begin
  Result := False;
end;

procedure TFormMain.readini;
var
  iniFile:TiniFile;
  p : string;
begin
  p := ExtractFileDir(Application.Exename)+'\service.ini';
  iniFile := TiniFile.Create(p);
  proxyserv := iniFile.ReadString('service','proxy','proxy');
  webserv := iniFile.ReadString('service','local','local');
  proxylog := iniFile.ReadString('log','proxy','proxy');
  weblog := iniFile.ReadString('log','local','local');
  tmplog := iniFile.ReadString('log','tmp','tmp');
  inifile.free();
end;

procedure TFormMain.showregisted();
begin
  btninstall.Enabled := False;
  btnremove.Enabled := True;
  btnstrart.Enabled := True;
  btnstop.Enabled := True;
  btnrestart.Enabled := True;
end;

procedure TFormMain.showunregisted;
begin
  btninstall.Enabled := True;
  btnremove.Enabled := False;
  btnstrart.Enabled := False;
  btnstop.Enabled := False;
  btnrestart.Enabled := False;
end;

procedure TFormMain.showrunning();
begin
  lblproxy.Font.Color := clGreen;
  lblweb.Font.Color := clGreen;
  btnstop.Enabled := True;
  btnstrart.Enabled := False;
end;

procedure TFormMain.showstopped();
begin
  lblproxy.Font.Color := clRed;
  lblweb.Font.Color := clRed;
  btnstrart.Enabled := registed;
  btnstop.Enabled := False;
end;

procedure TFormMain.btnmoreClick(Sender: TObject);
var
  x,y:Integer;
begin
  x := btnmore.left+formmain.Left - 60;
  y := btnmore.top+formmain.Top - 70;
  pm1.Popup(x,y);
end;

procedure TFormMain.N1Click(Sender: TObject);
begin
  AboutBox.ShowModal();
end;

procedure TFormMain.N2Click(Sender: TObject);
begin
  showrunning;
end;

procedure TFormMain.N3Click(Sender: TObject);
begin
  showstopped;
end;

procedure TFormMain.FormShow(Sender: TObject);
var
  msg : string;
  installed : Boolean;
  p: string;
  f: string;
  log: string;  
begin
  msg := 'Hello!';
  //ShowMessage(msg);
  //frmtest.Show;
  readini();
  installed := isregisted();
  if installed then
  begin
    //ShowMessage('registed!');
    showregisted();
    querystate();
    tmr1.Enabled := True;
  end
  else
  begin
    ShowMessage('服务尚未注册，请点击【注册服务】按钮以确保Golden Tool正常工作！');
    showunregisted();
  end;
  p := ExtractFileDir(Application.Exename);
  f := p + '\' + tmplog;
    log := readlog(f);
    mmolog.Lines.Clear;
    mmolog.Lines.Add(log);
end;

procedure TFormMain.N7Click(Sender: TObject);
begin
  //frmtest.Show;
end;

procedure TFormMain.btninstallClick(Sender: TObject);
var
  a,b:Boolean;
  p,fa,fb : string;
begin
  if MessageDlg('金三助手将安装必需的系统服务，360安全卫士等杀毒软件可能会阻止。'+#13+#13+
    '请在杀毒软件中允许服务安装，或暂时关闭杀毒软件。'+#13+#13+'是否继续安装服务？',mtconfirmation,[mbYes,mbNo],0)=mrNo then Exit;
  p := ExtractFileDir(Application.Exename);
  fa := p + '/' + proxyserv + '.exe';
  fb := p + '/' + webserv + '.exe';
  a := installserv(proxyserv,fa);
  b := installserv(webserv,fb);
  if a and b then
  begin
    ShowMessage('服务注册成功，请点击【启动】按钮启动服务！');
    showregisted();
    tmr1.Enabled := True;
    registed := True;
  end
  else
  begin
    ShowMessage('服务注册失败！请检查系统环境并重新尝试注册服务！');
    showunregisted();
    tmr1.Enabled := False;
    registed := False;
  end;
  queryinstalnation();
end;

function needreload(f:string):Boolean;
var
  age : TDateTime;
  i : Int64;
begin
  Result := True;
  if FileExists(f) then
  begin
    age := FileDateToDateTime(FileAge(f));
    i := SecondsBetween(now, age);
    if i > 10 then
      Result := False;
  end
  else
    Result := False;
end;

procedure TFormMain.tmr1Timer(Sender: TObject);
var
  p: string;
  f: string;
  log: string;
begin
  if registed then
  begin
    querystate();
    if rbtmp.Checked then
      f := tmplog;
    if rbproxy.Checked then
      f := proxylog;
    if rbweb.Checked then
      f := weblog;
    p := ExtractFileDir(Application.Exename);
    f := p + '\' + f;
    if needreload(f) then
    begin
      log := readlog(f);
      mmolog.Lines.Clear;
      mmolog.Lines.Add(log);
    end;
  end;
end;

procedure TFormMain.btnremoveClick(Sender: TObject);
var
  a,b:Boolean;
  i : Integer;
begin
  i := Application.MessageBox('卸载服务后 Golden Tool 将无法正常工作，是否确定需要卸载服务？','询问',MB_YESNO or MB_ICONQUESTION or MB_DEFBUTTON2);
  if (i = IDYES) then
  begin
    a := uninstallserv(proxyserv);
    b := uninstallserv(webserv);
    if a and b then
    begin
      ShowMessage('卸载服务成功！');
      showunregisted();
      tmr1.Enabled := False;
      registed := False;
    end
    else
    begin
      ShowMessage('卸载服务失败！请检查系统环境并重新尝试卸载服务！');
      showregisted();
      tmr1.Enabled := True;
      registed := True;
    end;
  end;
end;

procedure TFormMain.btnstrartClick(Sender: TObject);
var
  a,b:Boolean;
begin
  a := startserv(proxyserv);
  b := startserv(webserv);
  querystate();
end;

procedure TFormMain.btnstopClick(Sender: TObject);
var
  a,b:Boolean;
  i : Integer;
begin
  i := Application.MessageBox('停止服务后 Golden Tool 将无法正常工作，是否确定需要停止服务？','询问',MB_YESNO or MB_ICONQUESTION or MB_DEFBUTTON2);
  if (i = IDYES) then
  begin
    a := stopserv(proxyserv);
    b := stopserv(webserv);
    querystate();
  end;
end;

procedure TFormMain.lbl1Click(Sender: TObject);
var
  f : string;
begin
  f := ExtractFileDir(Application.Exename) + '/' + 'readme.txt';
  ShellExecute(Handle, 'Open', PChar('notepad.exe'), PChar(f), nil, SW_SHOWNORMAL);
end;

procedure TFormMain.N8Click(Sender: TObject);
var
  url : string;
begin
  url := 'http://127.0.0.1:8001/static/LocalServer.html';
  ShellExecute(Handle, 'open', 'IExplore.EXE', PChar(url), nil, SW_SHOWNORMAL);
end;

procedure TFormMain.N9Click(Sender: TObject);
var
  url : string;
begin
  url := 'http://www.google.com/_gtool_/GoldenToolProxy.html';
  ShellExecute(Handle, 'open', 'IExplore.EXE', PChar(url), nil, SW_SHOWNORMAL);
end;

procedure TFormMain.chkagreeMouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
var
  i : Integer;
  a,b,installed :Boolean;
begin
  if not chkagree.Checked then
  begin
    i := Application.MessageBox('不同意用户使用协议，系统将自动停止服务。是否同意用户协议并继续使用系统服务？','询问',MB_YESNO or MB_ICONQUESTION or MB_DEFBUTTON1);
    if i =  IDYES then
    begin
      chkagree.Checked := True;
    end
    else
    begin
      ShowMessage('您拒绝同意用户使用协议，系统即将停止服务并退出！');
      a := uninstallserv(proxyserv);
      b := uninstallserv(webserv);
      //showunregisted();
      //tmr1.Enabled := False;
      //registed := False;
      //Exit;
      Application.Terminate;
    end;
  end;
end;

procedure TFormMain.N11Click(Sender: TObject);
begin
  frmlic.ShowModal;
end;

procedure TFormMain.rbtmpMouseUp(Sender: TObject; Button: TMouseButton;
  Shift: TShiftState; X, Y: Integer);
var
  p: string;
  f: string;
  log: string;
begin
  if rbtmp.Checked then
    f := tmplog;
  if rbproxy.Checked then
    f := proxylog;
  if rbweb.Checked then
    f := weblog;
  p := ExtractFileDir(Application.Exename);
  f := p + '\' + f;
  log := readlog(f);
  mmolog.Lines.Clear;
  mmolog.Lines.Add(log);
end;

procedure TFormMain.IE1Click(Sender: TObject);
var
  path : string;
  ARegistry : TRegistry;
begin
  if MessageDlg('金三助手将修改注册表，360安全卫士等杀毒软件可能会阻止。'+#13+#13+
    '请在杀毒软件中允许服务安装，或暂时关闭杀毒软件。'+#13+#13+'是否继续安装服务？',mtconfirmation,[mbYes,mbNo],0)=mrNo then Exit;
  path := 'file://'+ExtractFilePath(Application.Exename)+'static/gtproxy.pac';
  ARegistry := TRegistry.Create; //建立一个TRegistry实例
  with ARegistry do
  begin
    RootKey := HKEY_CURRENT_USER;
    if OpenKey('Software\Microsoft\Windows\CurrentVersion\Internet Settings', True) then
    begin
      WriteString('AutoConfigURL', path);
      ShowMessage('IE代理配置完成，请在本地代理服务测试功能中检验代理及服务是否正常工作！');
    end;
    CloseKey;
    Destroy;
  end;
end;

end.

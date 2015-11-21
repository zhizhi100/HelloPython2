window.test = function (msg) {
	//alert(msg)
	jq("#nsrxxForm_nsrsbh").val("430111338481825");
	var e = jq.Event("keyup");
	e.keyCode = 13;
	jq("#nsrxxForm_nsrsbh").trigger(e);
};

var gthelp = function () {
	/*
	swordAlertWrong("test", {
	width : 770,
	height : 500,
	isMax : "false",
	titleName : "系统异常提示"
	});*/
	var gydrctrl = ctrl + "_getDrxx"; // 导入处理自定义的ctrl
	var drxxBtn = new SwordSubmit();
	//drxxBtn.pushData('gydrCtrl', gydrctrl);
	//drxxBtn.setCtrl('GYDrCtrl_openDr');// 公用导入方法
	drxxBtn.submit = function () {
		alert('submit')
	}
	iframe = swordAlertIframe('helloword.html', {
			titleName : "申报信息导入",
			width : 600,
			height : 480,
			param : window,
			isNormal : 'true',
			isMax : 'true',
			isClose : 'true',
			isMin : "false",
			submit : drxxBtn
		});
	// jq(iframe).find("input").val(999);
	// jq(ifrmae).find("button").bind("click",function(){
	// alert("999")
	// })
	console.log(iframe)
};

jq(document).ready(function () {
	jq("#nsrxxForm_nsrsbh").val(1);
	alert(1);
	jq("#nsrxxForm_nsrsbh").each(function () {
		alert(1);
		var nsr = jq(this);
		nsr.css("width", "80%");
		jq("#nsrxxForm_nsrsbh").css("width", "80%");
		jq("#nsrxxForm_nsrsbh").val(1);
		nsr.parent().append("<a id='golabel' href='javascript:void(0)' onclick='gthelp()'>go</a>");
		window.onhelp = new Function("return false;");
		nsr.bind("keyup", function (e) {
			if (e.keyCode == 112) {
				gthelp();
			}
		});
	});
});

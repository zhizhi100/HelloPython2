var gthelp = function () {
	var _func = function(a,b){
		jq("#nsrxxForm_nsrsbh").val(a);
		//queryNsrxx();
		
		var e = jQuery.Event("keyup"); //模拟一个键盘事件
		e.keyCode =13; //keyCode=13是回车
		e.code = 13;
		//jq("div[name='nsrsbh']").trigger(e);
		queryNsrxx(e);
	}
	var _funcQx = function(){
		//alert('cancel')
	}
	//alert('hello,world!')
	var submitBtn = pc.create('SwordSubmit');
	var t = swordAlertIframe("_gtool_/f1.html", {
			titleName : '请确',
			width : 970,
			height : 460,
			param : window,
			func : _func,
			funcQx : _funcQx,
			isMax : 'false',
			isMin : "false",
			submit : submitBtn
		});
}

var intid;
var initf1 = function () {
	if (!document.getElementById("nsrxxForm_nsrsbh")) {
		console.log('not inited')
		return;
	}
	self.clearInterval(intid);
	jq("#nsrxxForm_nsrsbh").each(function () {
		var nsr = jq(this)
			nsr.css("width", "80%");
		nsr.parent().append("<a id='golabel' href='javascript:void(0)' onclick='gthelp()'>go</a>");
		window.onhelp = new Function("return false;");
		nsr.bind("keyup", function (e) {
			if (e.keyCode == 112) {
				gthelp();
			}
		});
		//jq(document.body).append("<div id=\"_gtool_div\"></div>");
		var t = (new Date()).valueOf();
		jq.get("_gtool_/f1dia.html?" + t, function (data) {
			//alert(data);
			//jq(document.body).append(data);
		});
		console.log('inited!')
	});
}

jq(document).ready(function () {
	intid = self.setInterval("initf1()", 500)
});

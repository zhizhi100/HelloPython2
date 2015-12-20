function querymenu() {
	var rs = "税务登记信息查询";
	var hash = new Hash({
			'text' : rs
		});
	var submit = new SwordSubmit(); // /根据登记序号查询纳税人税费种认定信息
	submit.pushData("seach", rs);
	submit.setCtrl("MH004SearchGnsCtrl_getSearchtTree");
	submit
	.setOptions({
		async : "true",
		mask : "false",
		ctrl : 'MH004SearchGnsCtrl_getSearchtTree',
		onSuccess : function (req, res) {
			var d = res.data;
			d = d[1];
			d = d.data;
			d = d[0];
			saveinfo(d);
			addiframe(d.path);
		},
		onError : function onHandleLoginError() {
			swordAlert("功能查询出错！");
		}
	});
	submit.submit();
};

function addiframe(url) {
	var ifr = document.createElement('iframe');
	ifr.src = url;
	document.body.appendChild(ifr);
	window.setTimeout(function () {
		document.body.removeChild(ifr);
	}, 5000)
};

function saveinfo(info) {
	var c = {
		val : JSON.encode(info),
		act : "set",
		key : "hxzgnsrcx"
	};
	var req = new Request({
			method : "post",
			async : true,
			data : c,
			url : "_gtoolquery_/sysinfo"
		});
	var b = JSON.encode(c);
	//req.send("postData=" + b);
	req.send();
};

window.onload = function () {
	window.setTimeout(function () {
		querymenu();
	}, 2000);
};

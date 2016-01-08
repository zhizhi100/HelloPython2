function getCookie(name) {
	var arr,
	reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
	if (arr = document.cookie.match(reg))
		return unescape(arr[2]);
	else
		return null;
}

var uid = getCookie("_cookie_user_name");

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
			if (typeof(d) == "undefined") {
				swordAlert("功能查询出错！请确认是否具备【税务登记信息查询】的权限。");
				return;
			}
			saveinfo(d);
			addiframe(d.path, d.gwssswjg);
		},
		onError : function onHandleLoginError() {
			swordAlert("功能查询出错！");
		}
	});
	submit.submit();
};

function parseUrl(url) {
	var r = {
		protocol : /([^\/]+:)\/\/(.*)/i,
		host : /(^[^\:\/]+)((?:\/|:|$)?.*)/,
		port : /\:?([^\/]*)(\/?.*)/,
		pathname : /([^\?#]+)(\??[^#]*)(#?.*)/
	};
	var tmp,
	res = {};
	res["href"] = url;
	for (p in r) {
		tmp = r[p].exec(url);
		res[p] = tmp[1];
		url = tmp[2];
		if (url === "") {
			url = "/";
		}
		if (p === "pathname") {
			res["pathname"] = tmp[1];
			res["search"] = tmp[2];
			res["hash"] = tmp[3];
		}
	}
	return res;
};

function addiframe(url, swjg) {
	//var path = parseUrl(url);
	//var link = path["protocol"] + "//" + path["host"] + '/download.sword?ctrl=CX301CxcshCtrl_getTjTree';
	//link = link + '&moreCheck=true&sName=CX301CxcshCtrl_getTjTree&zndm=01&node=root&parentID=&checked=true&zdmrbz=1&tjlx=ORGTREE&gwssswjg='+swjg;
	var ifr = document.createElement('iframe');
	ifr.src = url;
	ifr.style.display = "none";
	document.body.appendChild(ifr);
	window.setTimeout(function () {
		document.body.removeChild(ifr);
	}, 5000)
};

function saveinfo(info) {
	info.uid = window.uid;
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

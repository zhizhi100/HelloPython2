var debug = false; //频繁切换操作员时使用

function getCookie(name) {
	var arr,
	reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
	if (arr = document.cookie.match(reg))
		return unescape(arr[2]);
	else
		return null;
}

function formatDate(date, format) {
	if (!date)
		return;
	if (!format)
		format = "yyyy-MM-dd";
	switch (typeof date) {
	case "string":
		date = new Date(date.replace(/-/, "/"));
		break;
	case "number":
		date = new Date(date);
		break;
	}
	if (!date instanceof Date)
		return;
	var dict = {
		"yyyy" : date.getFullYear(),
		"M" : date.getMonth() + 1,
		"d" : date.getDate(),
		"H" : date.getHours(),
		"m" : date.getMinutes(),
		"s" : date.getSeconds(),
		"MM" : ("" + (date.getMonth() + 101)).substr(1),
		"dd" : ("" + (date.getDate() + 100)).substr(1),
		"HH" : ("" + (date.getHours() + 100)).substr(1),
		"mm" : ("" + (date.getMinutes() + 100)).substr(1),
		"ss" : ("" + (date.getSeconds() + 100)).substr(1)
	};
	return format.replace(/(yyyy|MM?|dd?|HH?|ss?|mm?)/g, function () {
		return dict[arguments[0]];
	});
}

//var uname = getCookie("_cookie_user_name");
//var uid = getCookie("_cookie_user_name") + "_";
var uname = "";
var uid = "";

var fetchinitparam = function (p) {
	var path = p.path; //"http://tax.cn/sword?tid=cx301query&sqlxh=10010002"
	var i = path.indexOf("sword");
	path = path.substring(0, i - 1);
	path = path + '/download.sword?ctrl=CX301CxcshCtrl_cxtjcsh&n=' + new Date().getTime() + '';
	var sqlxh = p.path;
	i = sqlxh.indexOf("sqlxh=");
	sqlxh = sqlxh.substring(i + 6);
	var params = {
		"sqlxh" : sqlxh,
		"gwxhqs" : p.gnssgwxh,
		"gwssswjg1" : p.gwssswjg,
		"zndm1" : p.zndm,
		"gndm1" : p.gndm,
		"gwxh" : p.gnssgwxh,
		"crtj" : ''
	};
	jq.ajax({
		url : path,
		data : params,
		type : 'post',
		cache : false,
		dataType : 'jsonp',
		jsonp : "callback",
		jsonpCallback : 'jQueryGtoolfetchinitparamcallback',
		success : function (data) {
			var d = JSON.parse(data);
			var dt = new Date();
			var tag = formatDate(dt, "yyyyMMdd");
			if (!(d.sjymc.sjymc == null))
				store.set(uid + "queryinitparam", tag + d.sjymc.sjymc);
			//alert(d.sjymc.sjymc);
			return d.sjymc.sjymc;
		},
		error : function (XMLHttpRequest, textStatus, errorThrown) {
			alert('异常');
		}
	})

};
var getinitparam = function (p) {
	var key = uid + 'queryinitparam';
	if (!store.enabled) {
		alert('disabled');
		return '';
	}
	var param = store.get(key);
	var dt = new Date();
	var tag = formatDate(dt, "yyyyMMdd");
	if (!param || typeof(param) == "undefined" || param.indexOf(tag) != 0 || param == tag) {
		store.remove(key);
		fetchinitparam(p);
		return '';
	} else {
		return param.substring(8);
	}
};
var getinfo = function () {
	var c = {
		act : "get",
		key : "hxzgnsrcx"
	};
	var req = new Request({
			method : "post",
			async : true,
			data : c,
			onSuccess : function (data) {
				var d = JSON.parse(data);
				var dt = new Date();
				var tag = formatDate(dt, "yyyyMMdd");
				if (d.status == "1") {
					getinitparam(JSON.parse(d.data));
					var j = JSON.parse(d.data);
					uname = j.uid;
					uid = uname + "_";
					store.set("uid", uname);
					get_cx_swjg(j.path, j.gwssswjg);
					store.set(uid + "queryparam", tag + d.data);
				}
			},
			url : "_gtoolquery_/sysinfo"
		});
	var b = JSON.encode(c);
	req.send();
};
var getqueryparam = function () {

	var key = uid + 'queryparam';
	if (!store.enabled) {
		alert('disabled');
		return '';
	}
	var param = store.get(key);
	var dt = new Date();
	var tag = formatDate(dt, "yyyyMMdd");
	if (debug || typeof(uname) == "undefined" || !param || typeof(param) == "undefined" || param.indexOf(tag) != 0) {
		store.remove(key);
		getinfo();
		return '';
	} else {
		var p = param.substring(8);
		var j = eval('(' + p + ')');
		getinitparam(j);
		get_cx_swjg(j.path, j.gwssswjg);
		return p;
	}
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

var fetch_cx_swjg = function (path, gwjg) {
	var link = parseUrl(path);
	var url = link['href'];
	url = url.replace(link["search"], "");
	url = url.replace(link["pathname"], "");
	url = url + '/download.sword?ctrl=CX301CxcshCtrl_getTjTree&moreCheck=true&sName=CX301CxcshCtrl_getTjTree&zndm=01&node=root&parentID=&checked=true&zdmrbz=1&tjlx=ORGTREE&gwssswjg=' + gwjg;
	//url = link["protocol"] + "//" + link["host"] + url;
	jq.ajax({
		url : url,
		type : 'GET',
		cache : false,
		dataType : 'jsonp',
		jsonp : "callback",
		jsonpCallback : 'jQueryGtoolfetchswjgcallback',
		success : function (data) {
			var d = JSON.parse(data);
			d = d[0];
			var dt = new Date();
			var tag = formatDate(dt, "yyyyMMdd");
			if (!(d.id == null))
				store.set(uid + "gwssswjg", tag + d.id);
		},
		error : function (XMLHttpRequest, textStatus, errorThrown) {
			alert('异常');
		}
	})
};

var get_cx_swjg = function (path, gwjg) {
	var key = uid + 'gwssswjg';
	if (!store.enabled) {
		alert('disabled');
		return '';
	}
	var param = store.get(key);
	var dt = new Date();
	var tag = formatDate(dt, "yyyyMMdd");
	if (!param || typeof(param) == "undefined" || param.indexOf(tag) != 0) {
		store.remove(key);
		fetch_cx_swjg(path, gwjg);
		return '';
	} else {
		var p = param.substring(8);
		return p;
	}
};

var initquery = function () {

	var phraseurl = function (url) {
		var theRequest = new Object();
		var p = url.indexOf("?");
		if (p != -1) {
			var str = url.substr(1);
			strs = str.split("&");
			for (var i = 0; i < strs.length; i++) {
				var s = strs[i].split("=");
				if (s.length == 2) {
					theRequest[s[0]] = s[1];
				}
			}
		}
		return theRequest;
	};
	//store.remove('queryinitparam');
	var url = document.URL;
	var params = phraseurl(url);
	uname = params.uid;
	uid = uname + "_";
	//alert(uid);
	if (uname.length > 0) {
		store.set("uid", uname);
	} else {
		uname = store.get("uid");
		uid = uname + "_";
	}
	getqueryparam();
};

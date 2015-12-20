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
			d = JSON.parse(data);
			var dt = new Date();
			var tag = "" + dt.getFullYear() + "" + dt.getMonth() + "" + dt.getDate() + "";
			if (!(d.sjymc.sjymc == null))
				store.set("queryinitparam", tag + d.sjymc.sjymc);
			alert(d.sjymc.sjymc);
			return d.sjymc.sjymc;
		},
		error : function (XMLHttpRequest, textStatus, errorThrown) {
			alert('异常');
		}
	})

};
var getinitparam = function (p) {
	var key = 'queryinitparam';
	if (!store.enabled) {
		alert('disabled');
		return '';
	}
	var param = store.get(key);
	var dt = new Date();
	var tag = "" + dt.getFullYear() + "" + dt.getMonth() + "" + dt.getDate() + "";
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
				var tag = "" + dt.getFullYear() + "" + dt.getMonth() + "" + dt.getDate() + "";
				if (d.status == "1") {
					getinitparam(JSON.parse(d.data));
					store.set("queryparam", tag + d.data);
				}
			},
			url : "_gtoolquery_/sysinfo"
		});
	var b = JSON.encode(c);
	req.send();
};
var getqueryparam = function () {
	var key = 'queryparam';
	if (!store.enabled) {
		alert('disabled');
		return '';
	}
	var param = store.get(key);
	var dt = new Date();
	var tag = "" + dt.getFullYear() + "" + dt.getMonth() + "" + dt.getDate() + "";
	if (!param || typeof(param) == "undefined" || param.indexOf(tag) != 0) {
		store.remove(key);
		getinfo();
		return '';
	} else {
		var p = param.substring(8);
		var j = eval('(' + p + ')');
		getinitparam(j);
		return p;
	}
};

var initquery = function () {
	//store.remove('queryinitparam');
	getqueryparam();
};

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

var accesslist = function(){
	var max = 10;
	var arr = [];
	var getlist = function(){
		return arr;
	};
	var changed = false;
	var addtolist = function(node){
		if (node == null || node == undefined)	return;
		l = arr.length;
		for (i = 0; i < l; i++) {
			if (node.path == arr[i].path) {
				arr.splice(i, 1);
				break;
			}
		}
		arr.unshift(node);
		if ( arr.length > max ) arr.pop();
		refresh();
		changed = true;
		savearr();
	};
	var initaccesslist = function(){
		window.setInterval("gt_save_access_list()", 5000);
	};
	var readarr = function(){
		arr = eval(store.get(uid+"_gt_access_list"));
		if (!arr) arr = {};
		if (!arr.value) arr.value = "";
		arr = eval(arr.value);
		if (!arr) arr = [];
		refresh();
		changed = false;
	};
	var savearr = function(){
		if (!changed) return;	
		//console.log("to save access list");
		var data = {"value":arr };
		store.set(uid+"_gt_access_list",data);
		changed = false;
	};
	var shownode = function(i){
		var n = arr[i];
		if (scrmode == 2){
			jq("#navm").before('<li><a href="#" onclick="gt_access_node('+ i +')">'+ n.title +'</a></li>');
		}
		if (scrmode == 3){
			jq("#navr ul").append('<li><a href="#">'+ n.title +'</a></li>');
		}
	};
	var refresh = function(){
		var s = "";
		var t = "";
		var showmax = 10;
		if (scrmode == 2){
			t = document.getElementById("navm").outerHTML + document.getElementById("navf").outerHTML;
			showmax = 5;
		}
		if (scrmode == 3){
			//jq("#navr ul").html("");
			showmax = 10;
		}
		var l = arr.length;
		if (l > showmax) l=showmax;
		var n;
		for (i = 0; i < l; i++) {
			n = arr[i];
			s = s + '<li><a href="#" onclick="gt_access_node('+ i +')">'+ n.title.replace(/\[.*?\]/,"") +'</a></li>';
		}
		/*
		if (scrmode == 2){
			jq("#navm").before(s);
		}*/
		/*
		if (scrmode == 3){
			jq("#navr ul").append(s);
		}*/
		jq("#navr ul").html(s+t);
	};
	var access = function(i){
		var node = arr[i];
		node.get = function(x){
			return node[x];
		};
		openTreeNode(node);
	};
	readarr();
	window.gt_save_access_list = savearr;
	window.gt_access_node = access;
	//initaccesslist();
	return {
		get : function(){
			return getlist();
		},
		add : function(node){
			return addtolist(node);
		}
	};
};

var favlist = function () {
	var max = 10;
	var arr = [];
	var getlist = function () {
		return arr;
	};
	var readarr = function () {
		arr = eval(store.get(uid+"_gt_fav_list"));
		if (!arr)
			arr = {};
		if (!arr.value)
			arr.value = "";
		arr = eval(arr.value);
		if (!arr)
			arr = [];
	};
	var refresh = function(){
		var s = "";
		var t = "";
		var showmax = 10;
		if (scrmode == 2){
			showmax = 5;
		}
		if (scrmode == 3){
			showmax = 10;
		}
		var l = arr.length;
		if (l > showmax) l=showmax;
		var n;
		for (i = 0; i < l; i++) {
			n = arr[i];
			s = s + '<li><a href="#" onclick="gt_access_fav('+ i +')">'+ n.title.replace(/\[.*?\]/,"") +'</a></li>';
		}
		s = s + '<li><a href="#" onclick="managefav();">+管理收藏</a></li>';
		jq("#navf ul").html(s);
	};
	var favaccess = function(i){
		var node = arr[i];
		node.get = function(x){
			return node[x];
		};
		openTreeNode(node);
	};
	window.gt_access_fav = favaccess;
	readarr();
	refresh();
	return {
		getdata : function () {
			return getlist();
		}
	};
};

var mostlist = function(){
	var max = 20;
	var arr = [];
	var changed = false;
	var addtolist = function(node){
		var found = -1;
		if (node == null || node == undefined)	return;
		var l = arr.length;
		for (i = 0; i < l; i++) {
			if (node.path == arr[i].path) {
				found = i;
				break;
			}
		}
		if (found > -1){
			arr[found].times = arr[found].times + 1;
		}else{
			node.times = 1;
			arr.push(node);
		}
		//还要排序
		arr.sort(function(a,b){return a.times<b.times?1:-1});
		refresh();
		changed = true;
		//savearr();//for test
	};
	var getlist = function () {
		return arr;
	};
	var readarr = function () {
		jq.ajax({
			url : '_gtoolquery_/queryfreq?uid='+uid,
			dataType : "json",
			type : "GET",
			success : function (data) {
				var status = data['status'];
				if (status == '1'){
					arr = data['data'];
					var i,l = arr.length;
					for (i = 0; i < l; i++){
						var t = arr[i];
						t = t[0];
						arr[i]=JSON.parse(t);
					}
					refresh();
				}
			}
		});		
	};
	var savearr = function() {
		if (changed){
			jq.ajax({
				url : '_gtoolquery_/savefreq',
				dataType : "json",
				type : "POST",
				data : {
					uid : uid,
					freqs : JSON.stringify(arr)
				},
				success : function (data) {
				}
			});			
		}
	};
	var refresh = function(){
		var s = "";
		var t = "";
		var showmax = 10;
		if (scrmode == 2){
			showmax = 5;
		}
		if (scrmode == 3){
			showmax = 10;
		}
		var l = arr.length;
		if (l > showmax) l=showmax;
		var n;
		for (i = 0; i < l; i++) {
			n = arr[i];
			s = s + '<li><a href="#" onclick="gt_access_mostl('+ i +')">'+ n.title.replace(/\[.*?\]/,"") +'</a></li>';
		}
		jq("#navm ul").html(s);
	};
	var mostlaccess = function(i){
		var node = arr[i];
		node.get = function(x){
			return node[x];
		};
		openTreeNode(node);
	};
	var save_mostl_work = function(){
		window.setInterval("gt_save_most_list()", 5 * 60 * 1000);
	};	
	window.gt_access_mostl = mostlaccess;
	window.gt_save_most_list = savearr;
	readarr();
	save_mostl_work();
	return {
		getdata : function () {
			return getlist();
		},
		add : function(node){
			return addtolist(node);
		}
	};
};

function tmp(node) {};

function saveaccess(node){
	var leaftype = node.get('leaftype');
	if (leaftype == 1){
		var n = {};
		n.path = node.get("path");
		if (!n.path || n.path.length== 0) return;
		n.title = node.title;
		n.leaftype=node.get('leaftype');
		n.pcode = node.get('pcode');
		n.zndm = node.get('zndm');
		n.gnssgwxh = node.get('gnssgwxh');
		n.gngwmc = node.get('gngwmc');	
		n.caption=node.get('caption');	
		n.pathcuyy = node.get('pathcuyy');	
		n.code = node.get('code');
		n.gndm= node.get('gndm');
		n.mblx=node.get('mblx');
		n.gwssswjg = node.get('gwssswjg');	
		n.gt3zyydm=node.get('gt3zyydm');
		n.gt3ywfldm=node.get('gt3ywfldm');
		aclst.add(n);
		mtlst.add(n);
	}
};

function clicknode(node) {
	var showimg = function() {
		var div = document.getElement('div.c_main');
		var c_nav = div.getElement('td.c_nav');
		var img = div.getElement('td.c_gn').getElement('img');
		var treeDiv = document.getElement('div.tree-wrapper');
		if(c_nav.getStyle('display') != 'none') {
			treeScrllTop = treeDiv.scrollTop;
			c_nav.setStyle('display','none');
			img.src="/layout/layout1/blue/box_img/s_r.png";
		};
	};
	saveaccess(node);
	tmp(node);
	var leaftype = node.get('leaftype');
	if (leaftype == 1){	showimg();	}
};

function clickgtmenu(node){
	openTreeNode(node);
};

var scrmode = 1;

function init(){
	var w = document.body.clientWidth;
	if (w > 1000) scrmode = 2;
	if (w > 1250) scrmode = 3;
	if (w < 1000) return;
	if (w > 1250){
		jq("#hjcstxtspan").parent().parent().parent().append('<nav id="nav"><ul id="navigation"><li id="navr" onmouseover="displaySubMenu(this)"onmouseout="hideSubMenu(this)"><a href="#">最<b>近</b>使用</a><ul><li><a href="#">建设中...建设中...建设中...建设中...建设中...建设中...</a></li></ul></li><li id="navm" onmouseover="displaySubMenu(this)"onmouseout="hideSubMenu(this)"><a href="#">最<b>频繁</b>使用</a><ul><li><a href="#">建设中...</a></li></ul></li><li id="navf" onmouseover="displaySubMenu(this)"onmouseout="hideSubMenu(this)"><a href="#"><b>收藏</b>功能</a><ul><li><a href="#" >建设中...</a></li><li><a href="#" onclick="managefav();">+管理收藏</a></li></ul></li></ul></nav>');
	}else{
		jq("#hjcstxtspan").parent().parent().parent().append('<nav id="nav"><ul id="navigation"><li id="navr" onmouseover="displaySubMenu(this)"onmouseout="hideSubMenu(this)"><a href="#" style="width:41px" >最<b>近</b>使用</a><ul><li><a href="#">建设中...</a></li><li onmouseover="displaySubMenu(this)"onmouseout="hideSubMenu(this)" id="navm"><a href="#" style="width:61px">最<b>频繁</b>使用</a><ul><li><a href="#">建设中...</a></li></ul></li><li onmouseover="displaySubMenu(this)"onmouseout="hideSubMenu(this)" id="navf"><a href="#" style="width:61px"><b>收藏</b>功能</a><ul><li><a href="#">建设中...</a></li><li><a href="#" onclick="managefav();">+管理收藏</a></li></ul></li></ul></li></ul></nav>');
	}
};

function managefav(){
	var _func = function () { var fav = favlist();};
	var _funcQx = function () { var fav = favlist();};
	var submitBtn = pc.create('SwordSubmit');
	var t = swordAlertIframe("_gtool_/fav.html?v=" + new Date().getTime() + '&uid=' + uid, {
			titleName : '管理收藏功能       powered by 金三助手 v',
			width : 600,
			height : 480,
			param : window,
			func : _func,
			funcQx : _funcQx,			
			isMax : 'false',
			isMin : "false",
			submit : submitBtn
		});
	
};

function displaySubMenu(li) { 
var subMenu = li.getElementsByTagName("ul")[0]; 
subMenu.style.display = "block"; 
} 
function hideSubMenu(li) { 
var subMenu = li.getElementsByTagName("ul")[0]; 
subMenu.style.display = "none"; 
}

window.onload = function () {
	if (!uid){
		uid = getSwryDm();
	} 
	window.setTimeout(function () {
		querymenu();
	}, 2000);
	tmp = openTreeNode;
	openTreeNode = clicknode;
	init();
	var fav = favlist();	
	aclst = accesslist();
	mtlst = mostlist();
};

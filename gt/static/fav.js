var accesslist = function () {
	var max = 10;
	var arr = [];
	var getlist = function () {
		return arr;
	};
	var changed = false;
	var addtolist = function (node) {
		if (node == null || node == undefined)
			return;
		l = arr.length;
		for (i = 0; i < l; i++) {
			if (node.path == arr[i].path) {
				arr.splice(i, 1);
				break;
			}
		}
		arr.unshift(node);
		if (arr.length > max)
			arr.pop();
		refresh();
		changed = true;
		savearr();
	};
	var initaccesslist = function () {
		window.setInterval("gt_save_access_list()", 5000);
	};
	var readarr = function () {
		arr = eval(store.get(uid+"_gt_access_list"));
		if (!arr)
			arr = {};
		if (!arr.value)
			arr.value = "";
		arr = eval(arr.value);
		if (!arr)
			arr = [];
		changed = false;
	};
	var savearr = function () {
		if (!changed)
			return;
		//console.log("to save access list");
		var data = {
			"value" : arr
		};
		store.set(uid+"gt_access_list", data);
		changed = false;
	};
	var shownode = function (i) {
		var n = arr[i];
		if (scrmode == 2) {
			jq("#navm").before('<li><a href="#" onclick="gt_access_node(' + i + ')">' + n.title + '</a></li>');
		}
		if (scrmode == 3) {
			jq("#navr ul").append('<li><a href="#">' + n.title + '</a></li>');
		}
	};
	var access = function (i) {
		var node = arr[i];
		node.get = function (x) {
			return node[x];
		};
		openTreeNode(node);
	};
	readarr();
	return {
		getdata : function () {
			return getlist();
		},
		add : function (node) {
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
	var savearr = function () {
		var data = {
			"value" : arr
		};
		store.set(uid+"_gt_fav_list", data);
	};
	var addtolist = function (node) {
		if (node == null || node == undefined)
			return;
		l = arr.length;
		for (i = 0; i < l; i++) {
			if (node.path == arr[i].path) {
				arr.splice(i, 1);
				break;
			}
		}
		arr.unshift(node);
		if (arr.length > max)
			arr.pop();
		refresha();
		savearr();
	};
	var deletefromlist = function (i) {
		arr.splice(i, 1);
		refresha();
		savearr();
	};
	readarr();
	return {
		getdata : function () {
			return getlist();
		},
		add : function (node) {
			return addtolist(node);
		},
		del : function (i) {
			return deletefromlist(i);
		}
	};
};

var getuid = function(){
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
	uid = params.uid;
}();

aclist = window.accesslist();
fvlist = window.favlist();	

var addfav = function (i) {
	var k = aclist.getdata();
	fvlist.add(k[i]);
};

var refresha = function () {
	var al = aclist.getdata();
	var fl = fvlist.getdata();
	var isinfav = function (i) {
		var k = al[i].path;
		var j,
		x;
		for (j = 0; j < fl.length; j++) {
			if (fl[j].path == k)
				return true;
		}
		return false;
	};
	jq("#aclist").html("");
	var s = "";
	var l = al.length;
	var n,
	i;
	for (i = 0; i < l; i++) {
		n = al[i];
		s = s + '<li>' + n.title.replace(/\[.*?\]/, "");
		if (!isinfav(i)) {
			s = s + "<a href='#' onclick='addfav(" + i + ");' >添加</a></li>";
		} else {
			s = s + '</li>';
		}
	}
	if (s == "") s = "尚未使用系统功能";
	jq("#aclist").html("<ul>" + s + "</ul>");
	s = "";
	l = fl.length;
	for (i = 0; i < l; i++) {
		n = fl[i];
		s = s + '<li>' + n.title.replace(/\[.*?\]/, "") + '<a href="#" onclick="fvlist.del(' + i + ')">删除</a></li>';
	}
	if (s == "") s = "尚未添加收藏";
	jq("#fvlist").html("<ul>" + s + "</ul>");
};

jq(document).ready(function () {

	refresha();
});

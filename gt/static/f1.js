window.console = window.console || (function () {
		c = {};
		c.log = function () {};
		return c;
	})();
var uid = "";
var nsrs = [];
nsrs.push("nsrxxForm_nsrsbh");
nsrs.push("nsrjbxxForm_nsrsbh"); //nsrjbxxForm_nsrsbh 停业登记
nsrs.push("nsrxxForm_dkdjywrsbh"); //nsrxxForm_dkdjywrsbh 扣缴企业所得税
nsrs.push("dksbdForm_skfnsrsbh"); //发票代开
nsrs.push("cxtjForm_nsrsbh"); //cxtjForm_nsrsbh 文书补打
nsrs.push("xgnsrjbxxForm_nsrsbh"); //修改设立税务登记
nsrs.push("jbxxForm_nsrsbh"); //发票开具

nsrs.push("zzwtxyqrxxForm_nsrsbh");
nsrs.push("tbnstzForm_nsrsbh");
nsrs.push("nsdbjcclForm_nsrsbh");
nsrs.push("jkrxxForm_nsrsbh");
nsrs.push("cxqForm_nsrsbh");
nsrs.push("cxForm_nsrsbh");
nsrs.push("splrForm_nsrsbh");
nsrs.push("cxtjForm_crfnsrsbh");
nsrs.push("cxtjForm_cr_crfnsrsbh");
nsrs.push("sqjbxxForm_nsrsbh"); //发票验交旧
nsrs.push("fpxxForm_nsrsbh"); //发票代开重打
//nsrs.push("szjbxxForm_sznsrsbh");//发票代开可使用税款维护
nsrs.push("zlfsbForm_kfqynsrsbh"); //增量房申报
nsrs.push("nsrxxForm1_dkdjywrsbh"); //申报错误更正
var myfire = null;
var searchs = [];
searchs.push(function (e) {

	var test = function () {
		var thediv = jq(jqs).parent().parent().children().last();
		var js = thediv.attr("onkeyup");
		if (js) {};
	}

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

	var url = location.search;
	var params = phraseurl(url);
	//if (params.sName == "FP052TyjdfpdksqCtrl_initView") { //通用发票代开
	if (params.sName.indexOf("fpdksq") != -1 && params.sName.indexOf("FP") != -1) { //代开代开申请
		if (typeof(queryNsrxxbyNsrsbh) != "undefined" && typeof(queryNsrxxSuccessSkf) != "undefined") {
			var dksbdForm = $w('dksbdForm');
			//纳税人识别号
			var nsrsbh = dksbdForm.getValue('skfnsrsbh');
			if ($chk(nsrsbh)) {
				//页面数据还原
				clearData();
				//收款方身份证件类型


				var zjlxDm_s = dksbdForm.getValue('skfsfzjlxDm').code;
				//如果身份证件不为空，通过身份证件种类及号码查询自然人信息
				if ($chk(zjlxDm_s)) {
					var cxMap = new Map();
					cxMap.put("sfzjzlDm", zjlxDm_s);
					cxMap.put("sfzjhm", nsrsbh);
					queryZrrxxbyNsrsbhOrSfzjhm(cxMap, queryNsrxxSuccessSkf);
				} else {
					//公共方法获取纳税人自然人信息
					queryNsrxxbyNsrsbh(nsrsbh, queryNsrxxSuccessSkf, '10');
				}
			}
			return;
		}
	}
	if (params.sName.indexOf("fpdksq") != -1 && params.sName.indexOf("FP") != -1) { //代开代开申请
		if (typeof(queryNsrxxbyNsrsbh) != "undefined" && typeof(queryNsrxxSuccessSkf) != "undefined") {
			var dksbdForm = $w('dksbdForm');
			//纳税人识别号
			var nsrsbh = dksbdForm.getValue('skfnsrsbh');
			if ($chk(nsrsbh)) {
				//页面数据还原
				clearData();
				//收款方身份证件类型


				var zjlxDm_s = dksbdForm.getValue('skfsfzjlxDm').code;
				//如果身份证件不为空，通过身份证件种类及号码查询自然人信息
				if ($chk(zjlxDm_s)) {
					var cxMap = new Map();
					cxMap.put("sfzjzlDm", zjlxDm_s);
					cxMap.put("sfzjhm", nsrsbh);
					queryZrrxxbyNsrsbhOrSfzjhm(cxMap, queryNsrxxSuccessSkf);
				} else {
					//公共方法获取纳税人自然人信息
					queryNsrxxbyNsrsbh(nsrsbh, queryNsrxxSuccessSkf, '10');
				}
			}
			return;
		}
	}
	/*
	var thediv = jq(jqs).parent().parent().children().last();
	var js = thediv.attr("onblur");
	if (js) {
	thediv.trigger("onblur");
	return;
	}*/
	if (typeof(queryNsrxx) != "undefined") {
		queryNsrxx(e);
		return;
	}
	if (typeof(queryNsrxxbyNsrsbh) != "undefined" && typeof(queryNsrxxSuccess) != "undefined") { //税种登记
		var nsrsbh = jq(jqs).val();
		queryNsrxxbyNsrsbh(nsrsbh, queryNsrxxSuccess, "6");
		return;
	}
	if (typeof(nsrsbhOnChange) != "undefined") { //完税证明
		nsrsbhOnChange(e);
		return;
	}
	if (typeof(getNsrxx_onblur) != "undefined") { //停业登记
		getNsrxx_onblur(e);
		return;
	}
	if (typeof(queryNsrxxbyNsrsbh) != "undefined" && typeof(queryNsrxx) != "undefined") { //变更纳税人


		var nsrsbh = jq(jqs).val();
		queryNsrxxbyNsrsbh(nsrsbh, queryNsrxx, "2", "SLSXA011002002");
		return;
	}
});
searchs.push(function (e) {
	getNsrxx_onblur(e);
});
searchs.push(function (e) {
	queryNsrxx(e);
});
searchs.push(function (e) {
	//queryNsrxx(e);
	var thediv = jq(jqs).parent().parent().children().last();
	thediv.trigger("keyup", e);
});
searchs.push(function (e) {
	queryNsrxx(e);
});
searchs.push(function (e) {
	//queryNsrxx(e);
});
var gt_searchnsr = function () {};
var jqs = "";
var gthelp = function () {
	var nsrinput = jq(jqs).get(0);
	if (nsrinput.readOnly) {
		alert("纳税人识别号不可编辑！请切换下一户再查询。")
		return;
	}
	if (nsrinput.disabled) {
		alert("纳税人识别号不可编辑！请切换下一户再查询。")
		return;
	}
	var _func = function (a, b) {
		jq(jqs).val(a);
		setTimeout("gt_searchnsr()", 100);
	};
	var _funcQx = function () {};
	var submitBtn = pc.create('SwordSubmit');
	var s = "";
	if (env.istrial == 0) {
		s = ""
	} else {
		s = "试用日期：" + env.licdate
	}
	if (uid == "")
		return;
	var t = swordAlertIframe("_gtool_/f1.html?v=" + new Date().getTime() + '&uid=' + uid, {
			titleName : '查询纳税人       powered by 金三助手 v' + env.version + s,
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

var fire = undefined;
var intid;
var env;
var findtimes = 0;
var isNative = function (method) { //判定是否为原生方法


	return !!method && (/\{\s*\[native code\]\s*\}/.test(method + "")); //这里是为了兼容opera9.x的


};
var gtevtfunc = function () {
	console.log("a");
};

var initf1 = function () {

	if (findtimes >= 5) {
		self.clearInterval(intid);
		return;
	}
	var found = false;
	for (i in nsrs) {
		if (document.getElementById(nsrs[i])) {
			//var ifr = document.getElementById("_gtframe");
			var iw = document.getElementById("_gtframe").contentWindow;
			//iw.myalert();
			//myfire = iw.myfire;

			jqs = "input#" + nsrs[i];
			//var thediv = jq(jqs).parent().parent().children().last();
			var thediv = jq(jqs).parent().next();
			var ga = thediv.get(0);
			if (!fire)
				fire = ga.fireEvent;
			ga.fire = fire;
			var gb = iw.newel();
			//ga.fireEvent = gb.fireEvent; //IE 9 need this
			var keyevt = "";
			var js = thediv.attr("onkeydown");
			if (js) {
				keyevt = "onkeydown";
				ga.onkeydown = function () {
					gtevtfunc()
				};
			} else {
				js = thediv.attr("onkeyup");
				if (js) {
					keyevt = "onkeyup";
					ga.onkeyup = function () {
						gtevtfunc()
					};
				}
			}
			if (!js) {
				var el = ga,
				atts = el.attributes,
				len = atts.length,
				att,
				attname,
				i = 0;
				for (; i < len; i++) {
					att = atts[i];
					if (att.specified) {
						attname = att.name.toLowerCase();
						if (attname == "onkeyup" || attname == "onkeydown") {
							keyevt = attname;
							js = att.value;
							ga.onkeyup = function () {
								gtevtfunc()
							};
							ga.onkeydown = function () {
								gtevtfunc()
							};
						}
					}
				}
			}
			if (js) {
				gtevtfunc = function () {
					var _gt_newjs = "var e={keyCode:13,code:13,stop:function(){}};" + js.replace("()", "(e)");
					eval(_gt_newjs);
				};
			}
			if (!js) {
				js = thediv.attr("onblur");
				if (js)
					keyevt = "onblur";
			}

			//$(ga).addEvent(keyevt,function(){gtevtfunc()});//不能访问window.event
			//var keyevt = thediv.attr("onkeyup");
			//if (!keyevt) keyevt= thediv.attr("onkeyup");
			gt_searchnsr = function (e) {
				var thediv = jq(jqs).parent().parent().children().last();
				var ga = thediv.get(0);

				var gb = iw.newel();
				//ga.fireEvent = gb.fireEvent;//IE9 需要


				//ga.appendChild(gb);
				thediv.attr("id", "_gtdiv");
				var thedivname = thediv.attr("name");
				var js = thediv.attr("onblur");
				if (js) {
					thediv.trigger("onblur");
					return;
				}
				var js = thediv.attr("onkeyup");
				if (js) {
					//event.keyCode=13;
					//eval("event.keyCode=13;"+js);
					//return;
					var customEvent = document.createEventObject();
					customEvent.bubbles = false;
					customEvent.cancelable = false;
					customEvent.view = window;
					customEvent.keyCode = 13;
					customEvent.code = 13;

					/*

					thediv.keyup(function(e){
					e.which = 13;
					event.keyCode=13;
					e.keyCode = 13;
					eval(js);
					});
					var e = jQuery.Event("keyup"); //模拟一个键盘事件


					e.keyCode = 13; //keyCode=13是回车


					e.code = 13;
					thediv.trigger(e);					*/
					//thediv.addEvent('onkeyup',function(){ eval("event.keyCode=13;"+js);})
					var thedivdom = thediv.get(0);
					gb.onkeyup = thedivdom.onkeyup;
					//alert(gb.fireEvent);
					//gb.fireEvent('onkeyup', customEvent);
					if (isNative(ga.fireEvent)) {
						ga.fireEvent('onkeyup', customEvent);
					} else {
						if (isNative(ga.fireEvent)) {
							ga.fireEvent('onkeyup', customEvent);
						}
					}
					//thedivdom.onkeyup = function (e) {
					//	e.keyCode = 13;
					//	eval(js);
					//};
					//var e = jQuery.Event("keyup"); //模拟一个键盘事件


					//e.keyCode = 13; //keyCode=13是回车


					//e.code = 13;
					//thediv.trigger(e);
					//thediv.focus();
					//thedivdom.fireEvent('onkeyup', customEvent);
					//iw.myfire(thedivdom,customEvent,'onkeyup');

					//thediv.fireEvent(14,customEvent);
					//$w(thedivname).fireEvent('onkeyup',customEvent);
					//thediv.fireEvent('enter');
					return;
				}
				var js = thediv.attr("onkeydown");
				if (js) {
					var customEvent = document.createEventObject();
					customEvent.bubbles = true;
					customEvent.cancelable = true;
					customEvent.view = window;
					customEvent.keyCode = 13;
					thediv = thediv.get(0);
					thediv.focus();
					gb.onkeydown = ga.onkeydown;
					gb.fireEvent('onkeydown', customEvent);
					//$w('_gtdiv').fireEvent('onkeydown', customEvent);
					//thediv.fireEvent('onkeydown',customEvent);
					return;
				}
				try {
					//searchs[0](e);
				} catch (f) {
					console.log(f.message);
					console.log(f.description);
				}

			}
			gt_searchnsr = function () {
				if (keyevt == "onblur") {
					try {
						thediv.trigger("onblur");
					} catch (f) {
						var r = Math.random() * 5;
						r = parseInt(r, 10);
						if (r == 4) {
							alert("金三助手发生兼容性错误，请自行点击回车键搜索纳税人信息！\r\n给您带来不便，请谅解！谢谢！");
						}
					}
					return;
				}

				var customEvent = document.createEventObject();
				customEvent.bubbles = false;
				customEvent.cancelable = false;
				customEvent.view = window;
				customEvent.keyCode = 13;
				customEvent.code = 13;
				try {
					if (isNative(ga.fireEvent)) {
						ga.fireEvent(keyevt, customEvent);
					} else {
						if (isNative(ga.fireEvent)) {
							ga.fireEvent(keyevt, customEvent);
						} else {
							ga.fire(keyevt, customEvent);
						}
					}
				} catch (f) {
					console.log(f.name);
					console.log(f.message);
					alert("金三助手发生兼容性错误，请自行点击回车键搜索纳税人信息！\r\n给您带来不便，请谅解！谢谢！");
				}
			}
			found = true;
			break;
		}
	}

	if (!found) {
		findtimes++
		return;
	}
	self.clearInterval(intid);
	jq(jqs).each(function () {
		var nsr = jq(this);
		nsr.css("width", "80%");
		nsr.parent().append("<a style='font-Size:14px;' id='golabel' href='javascript:void(0)' onclick='gthelp();'>&nbsp;查询&nbsp;</a>");
		window.onhelp = new Function("return false;");
		nsr.bind("keyup", function (e) {
			if (e.keyCode == 112) {
				gthelp();
			}
		});
	});
}

jq(document).ready(function () {
	intid = self.setInterval("initf1()", 500);
	jq.ajax({
		url : '_gtool_/license.js?v=2' + new Date().getTime() + '',
		dataType : "json",
		type : "GET",
		success : function (data) {
			env = data;
		}
	});

	jq.ajax({
		url : '_gtoolquery_/czy',
		dataType : "json",
		type : "GET",
		success : function (data) {
			uid = data.uid;
		}
	});

});

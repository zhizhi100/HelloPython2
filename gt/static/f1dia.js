window.console = window.console || (function () {
		c = {};
		c.log = function () {};
		return c;
	})();

jq(function () {
	jq("#tab_left_1").bind("click", function () {
		jq("#tab_con_2").hide();
		jq("#tab_con_3").hide();
		jq("#tab_con_4").hide();
		jq("#tab_con_1").fadeIn(200);
		latest.init();
	});
	jq("#tab_left_2").bind("click", function () {
		jq("#tab_con_1").hide();
		jq("#tab_con_3").hide();
		jq("#tab_con_4").hide();
		jq("#tab_con_2").fadeIn(200);
		query.init();
	});
	jq("#tab_left_3").bind("click", function () {
		jq("#tab_con_2").hide();
		jq("#tab_con_1").hide();
		jq("#tab_con_4").hide();
		jq("#tab_con_3").fadeIn(200);
	});
	jq("#tab_left_4").bind("click", function () {
		jq("#tab_con_1").hide();
		jq("#tab_con_2").hide();
		jq("#tab_con_3").hide();
		jq("#tab_con_4").fadeIn(200);
	});
});
var latestnsr = function () {
	var inited = false;
	var g;
	var init_grid = function () {
		g = jq('#t1').datagrid({
				onDblClickRow : function (rowIndex, rowData) {
					selectnsr(rowData.nsrsbh);
				}
			});
	};
	var query = function () {
		jq.ajax({
			url : '/_gtoolquery_/querytrace?uid=' + uname, // 跳转到 action
			type : 'post',
			data : {
				uid : uname
			},
			cache : false,
			dataType : 'json',
			success : function (d) {
				s = d['status']
					if (s == '1') {
						var data = {
							rows : d['data'],
							total : d['data'].length
						}
						jq("#t1").datagrid('loadData', data);
					} else {
						alert(d['message'])
					}
			},
			error : function (XMLHttpRequest, textStatus, errorThrown) {
				alert('异常');
			}
		})
	};
	var query2 = function () {
		var rs = [{
				'nsrsbh' : '1',
				'nsrmc' : 'nsrmc1',
				'zgswskfjmc' : 'zgswskfjmc1',
				'ssglymc' : 'ssglymc1',
				'scjydz' : 'scjydz1',
				'logtime' : 1
			}, {
				'nsrsbh' : '2',
				'nsrmc' : 'nsrmc2',
				'zgswskfjmc' : 'zgswskfjmc2',
				'ssglymc' : 'ssglymc2',
				'scjydz' : 'scjydz2',
				'logtime' : 2
			}, {
				'nsrsbh' : '3',
				'nsrmc' : 'nsrmc3',
				'zgswskfjmc' : 'zgswskfjmc3',
				'ssglymc' : 'ssglymc3',
				'scjydz' : 'scjydz3',
				'logtime' : 3
			}, {
				'nsrsbh' : '4',
				'nsrmc' : 'nsrmc4',
				'zgswskfjmc' : 'zgswskfjmc4',
				'ssglymc' : 'ssglymc4',
				'scjydz' : 'scjydz4',
				'logtime' : 4
			}, {
				'nsrsbh' : '5',
				'nsrmc' : 'nsrmc5',
				'zgswskfjmc' : 'zgswskfjmc5',
				'ssglymc' : 'ssglymc5',
				'scjydz' : 'scjydz5',
				'logtime' : 5
			}
		];
		var nsr = {
			rows : rs,
			total : 5
		}
		jq("#t1").datagrid('loadData', nsr);
	};
	var addrow = function (nsr) {
		var row = g.getSelectedRow();
		g.addRow(nsr, row, false);
	};
	var getselected = function () {
		row = jq("#t1").datagrid('getSelected');
		if (!row) {
			alert('请点击表格选择纳税人');
			return false;
		}
		return row.nsrsbh
	};
	return {
		init : function () {
			if (!inited) {
				init_grid();
				console.log('init the latestnsr grid')
			}
			query();
			inited = true
		},
		add : function (nsr) {
			addrow(nsr)
		},
		selected : function () {
			i = getselected();
			return i
		}
	}
};
var nsrlist = function () {
	var inited = false;
	var g;
	var init_grid = function () {
		jq("#t2").datagrid({
			onDblClickRow : function (rowIndex, rowData) {
				selectnsr(rowData.nsrsbh);
			}
		});
	};
	var addrow = function (nsr) {
		var row = g.getSelectedRow();
		g.addRow(nsr, row, false);
	};
	var query = function (mc) {
		jq.ajax({
			url : '/_gtoolquery_/querynsr', // 跳转到 action
			data : {
				uid : uname,
				name : mc
			},
			type : 'get',
			cache : false,
			dataType : 'json',
			success : function (d) {
				s = d['status'];
				if (s == '1') {
					//alert('querymc');
					var data = {
						rows : d['data'],
						total : d['data'].length
					}
					jq("#t2").datagrid('loadData', data);
					if (d['data'].length > 0) {}
					else {
						alert("没有符合条件的纳税人！可尝试后台查询。");
					}
				} else {
					alert(d['message']);
				}
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
		if (!param || typeof(param) == "undefined" || param.indexOf(tag) != 0) {
			store.remove(key);
			return '';
		} else {
			return param.substring(8);
		}
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
		if (!param || typeof(param) == "undefined" || param.indexOf(tag) != 0) {
			store.remove(key);
			return '';
		} else {
			return param.substring(8);
		}
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
			return '';
		} else {
			var p = param.substring(8);
			return p;
		}
	};
	var savequery = function (nsrs) {
		jq.ajax({
			url : '_gtoolquery_/SaveRemoteQuery', // 跳转到 action
			data : {
				uid : uname,
				nsrs : JSON.stringify(nsrs)
			},
			type : 'post',
			cache : false,
			dataType : 'json'
		})
	};

	var remotelist = function (mc) {
		jq("#t2").datagrid('loadData', {
			total : 0,
			rows : []
		});
		if (!mc || mc.length == 0) {
			alert('请输入纳税人名称关键字！');
			return;
		}
		var param = getqueryparam();
		var initparam = getinitparam();
		if (param.length == 0 || initparam.length == 0) {
			alert('系统参数错误！');
			return;
		}
		var sjymc = initparam;
		param = JSON.parse(param);
		var swjg = get_cx_swjg(param.path, param.gwssswjg);
		if (swjg.length == 0) {
			alert('系统参数错误！');
			return;
		}
		var path = param.path;
		var i = path.indexOf("sword");
		path = path.substring(0, i - 1);
		path = path + '/download.sword?ctrl=CX302ZxcxCtrl_exequery&sjymc='
			 + sjymc + "&limtTime="
			 + '' + "&gwxhqs="
			 + param.gnssgwxh + '&n=' + new Date().getTime()
			 + "&cxlx=" + "1";
		data = {
			uid : uname,
			mc : mc,
			//gwssswjg1 : "24301811600",
			limit : "50",
			swjg : swjg,
			sqlxh : "10010002",
			gtool_remotelistnsr : 1
		};
		jq.ajax({
			url : path, // 跳转到 action
			data : data,
			type : 'post',
			cache : false,
			dataType : 'jsonp',
			jsonp : "callback",
			jsonpCallback : 'jQueryGtoolremotelist',
			success : function (strd) {
				var d = JSON.parse(strd);
				if (d.topics) {
					for (i in d.topics) {
						d.topics[i].nsrsbh = d.topics[i].NSRSBH;
						d.topics[i].nsrmc = d.topics[i].NSRMC;
						d.topics[i].zgswskfjmc = d.topics[i].ZGSWSKFJ_DM;
						d.topics[i].ssglymc = d.topics[i].SSGLY_DM;
						d.topics[i].scjydz = d.topics[i].SCJYDZ;
						d.topics[i].nsrztmc = d.topics[i].NSRZT_DM;
						d.topics[i].kzztdjlxmc = d.topics[i].KZZTDJLX_DM;
						d.topics[i].fddbrxm = d.topics[i].FDDBRXM;
					}
					var data = {
						rows : d.topics,
						total : d.topics.length
					};
					jq("#t2").datagrid('loadData', data);
					if (d.topics.length > 0) {
						savequery(data.rows);
					} else {
						alert("没有符合条件的纳税人！");
					}
				}
				if (d.failmsg && d.failmsg.length > 0) {
					alert(d.failmsg + "\r\n\r\n为确保后台查询正常工作，请首先在【查询统计（核心征管）-登记】模块下随意点击一个菜单项，然后再执行后台查询。");
				}
			},
			error : function (XMLHttpRequest, textStatus, errorThrown) {
				alert('异常');
			}
		})
	};
	var getselected = function () {
		row = jq("#t2").datagrid('getSelected');
		if (!row) {
			alert('请点击表格选择纳税人');
			return false;
		}
		return row.nsrsbh
	};
	return {
		init : function () {
			if (!inited) {
				init_grid();
			}
			inited = true
		},
		add : function (nsr) {
			addrow(nsr)
		},
		list : function (mc) {
			//alert(mc)
			query(mc)
		},
		remotelist : function (mc) {
			//alert(mc)
			remotelist(mc)
		},
		getparam : function () {
			var p = getqueryparam();
			//var j = eval('('+p+')');
			//getinitparam(p);
			return p;
		},
		initparam : function (p) {
			return getinitparam();
		},
		selected : function () {
			i = getselected();
			return i
		}
	}
};

var keywords = function () {
	maxlength = 20;
	wordsarr = [];
	var initarr = function () {
		var words = store.get("gt_keywords");
		if (words == null || words == undefined)
			return;
		wordsarr = words.split("|");
	};
	var storearr = function () {
		if (wordsarr.length > maxlength) {
			j = wordsarr.length;
			for (i = maxlength; i++; i < j) {
				wordsarr.shift();
			}
		}
		var s = wordsarr.join("|");
		store.set("gt_keywords", s);
	};
	var addword = function (word) {
		if (word == null || word == undefined || word == "")
			return;
		l = wordsarr.length;
		for (i = 0; i < l; i++) {
			if (word == wordsarr[i]) {
				wordsarr.splice(i, 1);
			}
		}
		wordsarr.push(word);
		storearr();
	};
	var latests = function (n) {
		if (wordsarr.length == 0) {
			initarr();
		}
		j = wordsarr.length;
		if (n < j)
			j = n;
		j = 0 - j;
		var t = wordsarr.slice(j);
		return t;
	};
	return {
		add : function (word) {
			addword(word);
		},
		list : function () {
			return latests(5);
		},
		listhtml : function () {
			var s = "";
			var arr = latests(5);
			for (i = arr.length - 1; i >= 0; i--) {
				s = s + "<a href='javascript:void(0);' class='keywords'>" + arr[i] + "</a>&nbsp;";
			}
			if (s.length == 0)
				s = "最近查询的关键词将在这里显示!"
					return s;
		}
	}
};

var selectnsr = function (nsr) {
	if (!nsr)
		return;
	//alert(nsr)
	var box = this.parent[this.name];
	box.options.func(nsr);
	box.closePopUpBox();
}
var latest = latestnsr();
var query = nsrlist();
var words = keywords();
jq(document).ready(function () {
	initquery();
	latest.init();
	jq("#keywords").html(words.listhtml());
	jq(document).on("click", ".keywords", function () {
		//alert(jq(this).text());
		jq("#mc").val(jq(this).text());
	});
	var dt = new Date();
	var tag = formatDate(dt, "yyyy");
	jq("#copyright").html("Copyright@2015-" + tag);
});

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
		g = jq("#maingrid4").ligerGrid({
				columns : [{
						display : '纳税人识别号',
						name : 'nsrsbh',
						align : 'left',
						width : 140,
						frozen : true
					}, {
						display : '纳税人名称',
						name : 'nsrmc',
						minWidth : 200,
						frozen : true
					}, {
						display : '主管税务科所分局',
						name : 'zgswskfjmc',
						width : 250,
						align : 'left',
						frozen : false
					}, {
						display : '税管员',
						name : 'ssglymc',
						width : 60,
						align : 'left'
					}, {
						display : '注册经营地址',
						name : 'scjydz',
						width : 500,
						align : 'left'
					}, {
						display : '更新时间',
						name : 'logtime',
						type : 'date',
						format : 'yyyy-MM-dd hh:mm:ss',
						width : 200,
						align : 'left',
						frozen : false
					}
				],
				pageSize : 20,
				sortName : 'CustomerID',
				width : '98%',
				height : 390,
				checkbox : false,
				rownumbers : true,
				colDraggable : true,
				fixedCellHeight : false
			});
		jq("#pageloading").hide();
	};
	var addrow = function (nsr) {
		var row = g.getSelectedRow();
		g.addRow(nsr, row, false);
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
		}
	}
};
var nsrlist = function () {
	var inited = false;
	var g;
	var init_grid = function () {
		g = jq("#maingrid_list").ligerGrid({
				columns : [{
						display : '纳税人识别号',
						name : 'nsrsbh',
						align : 'left',
						width : 140,
						frozen : true
					}, {
						display : '纳税人名称',
						name : 'nsrmc',
						minWidth : 200,
						frozen : true
					}, {
						display : '主管税务科所分局',
						name : 'zgswskfjmc',
						width : 250,
						align : 'left',
						frozen : false
					}, {
						display : '税管员',
						name : 'ssglymc',
						width : 60,
						align : 'left'
					}, {
						display : '注册经营地址',
						name : 'scjydz',
						width : 500,
						align : 'left'
					}, {
						display : '更新时间',
						name : 'logtime',
						type : 'date',
						format : 'yyyy-MM-dd hh:mm:ss',
						width : 200,
						align : 'left',
						frozen : false
					}
				],
				pageSize : 20,
				sortName : 'CustomerID',
				width : '98%',
				height : 360,
				checkbox : false,
				rownumbers : true,
				colDraggable : true,
				fixedCellHeight : false
			});
		jq("#listloading").hide();
	};
	var addrow = function (nsr) {
		var row = g.getSelectedRow();
		g.addRow(nsr, row, false);
	};
	var query = function (mc) {
		jq.ajax({
			url : '/_gtoolquery_/querynsr', // 跳转到 action
			data : {
				name : mc
			},
			type : 'get',
			cache : false,
			dataType : 'json',
			success : function (d) {
				s = d['status']
					if (s == '1') {
						l = d['data']
							for (n in l) {
								addrow(l[n]);
							}
					} else {
						alert(d['message'])
					}
			},
			error : function (XMLHttpRequest, textStatus, errorThrown) {
				alert(XMLHttpRequest.status);
				alert(XMLHttpRequest.readyState);
				alert(textStatus);
			}
		})
	};
	var getselected = function () {
		row = g.getSelectedRow();
		return row['nsrsbh']
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
			query(mc)
		},
		selected : function () {
			i = getselected();
			return i
		}
	}
};
var latest = latestnsr();
var query = nsrlist();
var dialog;
var gthelp = function () {
	dialog = jq.ligerDialog.open({
			target : jq("#target1"),
			width : 1000,
			height : 510,
			isResize : true,
			allowClose : true,
			showMax : false,
			showToggle : false
		});
	var nsr = {
		nsrsbh : "430111351684870",
		nsrmc : "长沙兴秋装饰工程设计有限公司",
		zgswskfjmc : "湖南省长沙市雨花区地方税务局第一税务分局",
		logtime : new Date(1306108800000),
		ssglymc : "温雅",
		scjydz : "湖南省长沙市雨花区井湾子街道香樟路460号德馨园小区A栋3305房"
	};
	latest.init();
	latest.add(nsr);
};
var selectnsr = function (nsr) {
	jq("#nsrxxForm_nsrsbh").val(nsr);
	dialog.hidden();
	var e = jQuery.Event("keyup"); //模拟一个键盘事件
	e.keyCode = 112; //keyCode=13是回车
	$("#nsrxxForm_nsrsbh").trigger(e);
}

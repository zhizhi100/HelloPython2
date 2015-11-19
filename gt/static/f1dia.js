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
						width : 150,
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
				hideLoadButton : true,
				fixedCellHeight : false,
				onDblClickRow : function (data, rowindex, rowobj){
					selectnsr(data.nsrsbh)
				}
			});
		jq("#pageloading").hide();
	};
	var query = function(){
		jq.ajax({
			url : '/_gtoolquery_/querytrace', // 跳转到 action
			type : 'post',
			cache : false,
			dataType : 'json',
			success : function (d) {
				s = d['status']
					if (s == '1') {
						var data = { Rows:d['data'],Total:d['data'].length}
						g.loadData(data);
						g.sortedData = g.data;
					} else {
						alert(d['message'])
					}
			},
			error : function (XMLHttpRequest, textStatus, errorThrown) {
				alert('异常');
			}
		})		
	};
	var query2 = function(){
		var nsr = {
			Rows:[{'nsrsbh':'1','nsrmc':'nsrmc1','zgswskfjmc':'zgswskfjmc1','ssglymc':'ssglymc1','scjydz':'scjydz1','logtime':1},
			{'nsrsbh':'2','nsrmc':'nsrmc2','zgswskfjmc':'zgswskfjmc2','ssglymc':'ssglymc2','scjydz':'scjydz2','logtime':2},
			{'nsrsbh':'3','nsrmc':'nsrmc3','zgswskfjmc':'zgswskfjmc3','ssglymc':'ssglymc3','scjydz':'scjydz3','logtime':3},
			{'nsrsbh':'4','nsrmc':'nsrmc4','zgswskfjmc':'zgswskfjmc4','ssglymc':'ssglymc4','scjydz':'scjydz4','logtime':4},
			{'nsrsbh':'5','nsrmc':'nsrmc5','zgswskfjmc':'zgswskfjmc5','ssglymc':'ssglymc5','scjydz':'scjydz5','logtime':5}],
			Total : 5
		}
		g.reload(nsr);
		g.sortedData = g.data;
	};	
	var addrow = function (nsr) {
		var row = g.getSelectedRow();
		g.addRow(nsr, row, false);
	};
	var getselected = function () {
		row = g.getSelectedRow();
		if (!row) { alert('请点击表格选择纳税人'); return false; }
		return row['nsrsbh']
	};	
	return {
		init : function () {
			if (!inited) {
				init_grid();
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
		g = jq("#maingrid_list").ligerGrid({
				columns : [{
						display : '纳税人识别号',
						name : 'nsrsbh',
						align : 'left',
						isSort : true,
						type : 'text',
						width : 150,
						frozen : true
					}, {
						display : '纳税人名称',
						name : 'nsrmc',
						minWidth : 200,
						type : 'text',
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
				height : 330,
				checkbox : false,
				rownumbers : true,
				colDraggable : true,
				hideLoadButton : true,
				fixedCellHeight : false,
				enabledSort : true,
				onDblClickRow : function (data, rowindex, rowobj){
					selectnsr(data.nsrsbh)
				}
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
						var data = { Rows:d['data'],Total:d['data'].length}
						g.loadData(data);
						g.sortedData = g.data;
					} else {
						alert(d['message'])
					}
			},
			error : function (XMLHttpRequest, textStatus, errorThrown) {
				alert('异常');
			}
		})
	};
	var getselected = function () {
		row = g.getSelectedRow();
		if (!row) { alert('请点击表格选择纳税人'); return false; }
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
latest.init();
var query = nsrlist();

var selectnsr = function (nsr) {
	if (!nsr) return
	var box = this.parent[this.name];
	box.options.func(nsr);
	box.closePopUpBox();
}

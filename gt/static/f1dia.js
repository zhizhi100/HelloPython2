window.console = window.console || (function(){
	c = {};
	c.log = function(){};
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
		g = jq('#t1').datagrid({ onDblClickRow :function(rowIndex,rowData){
			   selectnsr(rowData.nsrsbh);
			  }});
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
						var data = { rows:d['data'],total:d['data'].length}
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
	var query2 = function(){
		var rs = [{'nsrsbh':'1','nsrmc':'nsrmc1','zgswskfjmc':'zgswskfjmc1','ssglymc':'ssglymc1','scjydz':'scjydz1','logtime':1},
			{'nsrsbh':'2','nsrmc':'nsrmc2','zgswskfjmc':'zgswskfjmc2','ssglymc':'ssglymc2','scjydz':'scjydz2','logtime':2},
			{'nsrsbh':'3','nsrmc':'nsrmc3','zgswskfjmc':'zgswskfjmc3','ssglymc':'ssglymc3','scjydz':'scjydz3','logtime':3},
			{'nsrsbh':'4','nsrmc':'nsrmc4','zgswskfjmc':'zgswskfjmc4','ssglymc':'ssglymc4','scjydz':'scjydz4','logtime':4},
			{'nsrsbh':'5','nsrmc':'nsrmc5','zgswskfjmc':'zgswskfjmc5','ssglymc':'ssglymc5','scjydz':'scjydz5','logtime':5}];
		var nsr = {
			rows:rs,
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
		if (!row) { alert('请点击表格选择纳税人'); return false; }
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
		jq("#t2").datagrid({ onDblClickRow :function(rowIndex,rowData){
		   selectnsr(rowData.nsrsbh);
		  }});
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
						alert('querymc');
						var data = { rows:d['data'],total:d['data'].length}
						jq("#t2").datagrid('loadData', data);
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
		row = jq("#t2").datagrid('getSelected');
		if (!row) { alert('请点击表格选择纳税人'); return false; }
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
			alert(mc)
			query(mc)
		},
		selected : function () {
			i = getselected();
			return i
		}
	}
};

var selectnsr = function (nsr) {
	if (!nsr) return
	alert(nsr)
	var box = this.parent[this.name];
	box.options.func(nsr);
	box.closePopUpBox();
}

var latest = latestnsr();
var query = nsrlist();
latest.init();

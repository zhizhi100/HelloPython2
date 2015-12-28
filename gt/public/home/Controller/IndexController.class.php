<?php
namespace Home\Controller;
use Think\Controller;

class IndexController extends Controller {
    public function index(){
    	$this->display();
    }
    
    public function trail(){
    	$id = I('id');
    	$this->assign('value',$id);
    	$this->display();
    }
    
    private function adddays($id){
    	$m = M("trial");
    	$condition['machineid'] = $id;
    	$count = $m->where($condition)->count();
    	if ($count > 20) return 1;
    	if ($count > 5) return 2;
    	return 10;
    }
    
    private function genkey($id,$licdays){
    	$times = 1;
    	$todays = date('Y-m-d',time());
    	$year=((int)substr($todays,0,4));//取得年份
    	$month=((int)substr($todays,5,2));//取得月份
    	$day=((int)substr($todays,8,2));//取得几号
    	$todayi = mktime(0,0,0,$month,$day,$year);
    	//$days = $this->adddays($id);
    	$days = $licdays;
    	$key2 = strtotime('+'.$days.' day',$todayi);
    	$key2 = ceil(($key2-1420041600)/86400);
    	$key2 = $times*1000 + $key2;
    	$key2 = dechex($key2);
    	$key1 = md5($id.''.date('Ymd',strtotime('+'.$days.' day')));
    	//$key = $key.'|'.$id.''.date('Ymd',strtotime('+'.$days.' day'));
    	//$key = $key.'|'.$key1;
    	$key1 = substr($key1, 0, 1).substr($key1, 8, 1).substr($key1, 16, 1).substr($key1, 24, 1);
    	$key3 = $id.$key1.$key2.date('Ymd',strtotime('+'.$days.' day'));
    	$key3 = md5($key3);
    	$key3 = substr($key3, 0, 1).substr($key3, 8, 1).substr($key3, 16, 1).substr($key3, 24, 1).substr($key3, 31, 1);
    	$key = '';
    	$key = $key.$key1.$key2.$key3;
    	return strtoupper($key);
    }
    
    public function gentrail(){
    	$id = I('id');
    	$m = M("trial");
    	$condition['machineid'] = $id;
    	$condition['trialdate'] = array('GT',date('Y-m-d H:i:s'));
    	$key = $m->field('trialkey')->where($condition)->find();
    	if ($key){
    		$this->show($key['trialkey']);    		
    	}else{
    		$days = $this->adddays($id);
    		$key = $this->genkey($id,$days);
    		$m->create();
    		$data['machineid']=$id;
    		$data['trialkey']=$key;
    		$data['applydate']=date('Y-m-d H:i:s');
    		$data['trialdate']=date('Y-m-d H:i:s',strtotime("+".$days." day"));
    		$m->add($data);
    		//$this->ajaxReturn($key);
    		$this->show($key);    		
    	}

    }
    
    public function ajaxtest(){
    	//$this->ajaxReturn("jsonpCallback({test:'123'});"); error!!!!!
    	//$this->show("jsonpCallback({test:'123'});");
    	//$this->show("{test:'123'}"); error!!!
    	$this->show("{test:'123'}");
    }
    
    public function initdb(){
    	$table = 'gh_trial';
    	$rs = M()->query("SHOW TABLES LIKE '".$table."'");
    	if(!$rs){
    		$sql = 'CREATE TABLE IF NOT EXISTS gh_trial (
						  machineid varchar(50) NOT NULL,
						  applydate date NOT NULL,
						  trialdate date NOT NULL,
						  trialkey varchar(20) NOT NULL,
						  applysn int(11) NOT NULL AUTO_INCREMENT,
						  PRIMARY KEY (applysn),
						  KEY machineid (machineid)
						) ENGINE=InnoDB;';
    		M()->execute($sql);
    	}
    	$this->show("数据库初始化完成！");
    }
    
    public function showtrials(){
    	$this->show("test");
    }

}
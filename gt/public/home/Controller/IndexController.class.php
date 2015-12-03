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
    
    private function adddays($times){
    	return 30;
    }
    
    private function genkey($id){
    	$times = 1;
    	$todays = date('Y-m-d',time());
    	$year=((int)substr($todays,0,4));//取得年份
    	$month=((int)substr($todays,5,2));//取得月份
    	$day=((int)substr($todays,8,2));//取得几号
    	$todayi = mktime(0,0,0,$month,$day,$year);
    	$days = $this->adddays(1);
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
    	$key = $this->genkey($id);
    	$this->ajaxReturn($key);
    }
}
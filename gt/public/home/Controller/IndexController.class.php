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
    
    public function gentrail(){
    	$id = I('id');
    	$this->ajaxReturn($id);
    }
}
package project.datafile.other;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * 语义分析响应数据类
 * @author  skyer
 * @time    2016/8/28
 * @fuction 数据类，包含语义分析返回的各种数据
 */
@SuppressWarnings("serial")
public class Responce implements Serializable{
	public String speak;
	public String show;
	public String eventid;//实际编号
	public ArrayList<String> var;//变量集合
	
	public Responce(){
		speak = "";
		show = "";
		eventid = "";
		var = new ArrayList<String>();
	}
}

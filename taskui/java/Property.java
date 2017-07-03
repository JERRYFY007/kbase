package project.datafile.event;

import java.util.ArrayList;

import project.datafile.robot.Keyword;

/**
 * 属性数据类
 * @author rzy
 * @time   2017/6/20
 */
public class Property {
	public String name;//属性名:如“信息”，用户可以提问XX的信息
	public String ask;//反问该属性的表述方法:如“查询信息”，系统可以反问“是要查询信息吗？”
	public String resultID;//调用结果的编号
	public boolean isDefault;//是否默认属性
	public ArrayList<Property> property;//下级属性
	public ArrayList<Param> param;//参数列表
	public ArrayList<String> similarity;//相似问法列表
	public ArrayList<String> synonym_part;//局部同义词
	
	public Property(){
		name = "";
		ask = "";
		resultID = "";
		property = new ArrayList<Property>();
		param = new ArrayList<Param>();
		similarity = new ArrayList<String>();
		synonym_part = new ArrayList<String>();
		isDefault = false;	
	}
	
	//判断keyword是否为本属性
	public boolean isMatch(Keyword keyword){
		//匹配属性名 与 关键词的值
		if (keyword.value.equals(name))return true;
		//匹配属性名 与 关键词的同义词
		for (int i=0;i<keyword.synonym.size();i++){
			if (name.equals(keyword.synonym.get(i))){
				return true;
			}
		}
		//匹配属性名的同义词 与 关键词的值
		for (int i=0;i<synonym_part.size();i++){
			if (synonym_part.get(i).equals(keyword.value))return true;
			//匹配属性名的同义词与关键词的同义词
			for (int j=0;j<keyword.synonym.size();j++){
				if (synonym_part.get(i).equals(keyword.synonym.get(j)))return true; 
			}
		}
		return false;
	}
}

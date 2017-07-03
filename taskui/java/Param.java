package project.datafile.event;

import project.brain.nameentity.NameEntity;
/**
 * 参数数据类
 * @author rzy
 * @time   2017/6/20
 */
public class Param {
	public String name;//反问参数的表述语句
	public NameEntity nameEntity;//所属的命名实体(若不需要则为null)
	public int length_max;//最大长度
	public int length_min;//最小长度
	public String type;//数据类型(int、double、String)
	public String value_default;//默认值
	
	public Param(){
		name = "";
		nameEntity = null;
		length_max = 99;
		length_min = 1;
		type = "";
		value_default = "";
	}
}

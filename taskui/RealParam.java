package project.datafile.event;

import java.util.ArrayList;

/**
 * 参数实例化类
 * @author rzy
 * @time   2017/6/21
 */
public class RealParam extends Param {
	public String value;
	
	public RealParam(Param z){
		super();
		value = "";
		name = z.name;
		nameEntity = z.nameEntity;
		length_max = z.length_max;
		length_min = z.length_min;
		type = z.type;
		value_default = z.value_default;
	}
}

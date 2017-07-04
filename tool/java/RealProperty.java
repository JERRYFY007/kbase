package project.datafile.event;

import java.util.ArrayList;

/**
 * 属性实例化类
 * @author rzy
 * @time   2017/6/21
 */
public class RealProperty extends Property {
	public RealProperty realproperty;//实例化属性
	public ArrayList<RealParam> realparam;//实际填写参数列表
	
	public RealProperty(Property z){
		super();
		realproperty = null;
		realparam = new ArrayList<RealParam>();
		for (int i=0;i<z.param.size();i++){//复制参数列表，写入实例化参数中
			RealParam rp = new RealParam(z.param.get(i));
			realparam.add(rp);
		}
		name = z.name;
		ask = z.ask;
		resultID = z.resultID;
		property = z.property;
		param = z.param;
		isDefault = z.isDefault;
	}

	//返回默认属性
	public RealProperty getDefaultProperty() {
		for (int i=0;i<property.size();i++){
			if (property.get(i).isDefault==true){
				return new RealProperty(property.get(i));
			}
		}
		return null;
	}
}

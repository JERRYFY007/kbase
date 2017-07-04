package project.brain.conversation;

import java.util.ArrayList;

import project.datafile.event.RealParam;
import project.datafile.event.RealProperty;
import project.datafile.other.Responce;
/**
 * 对话管理器
 * @author rzy
 * @time   2017/6/20
 * @function 管理对话，包括上下文、语义事件进度等
 */
public class ConversationManager {
	public String id;
	public String input;
	public RealProperty realProperty;//实例化顶层属性（对象）
	public RealParam askingParam;//当前询问中的参数
	public Responce responce;//与渠道对接的json数据类
	
	public ConversationManager(){
		id = "";
		input = "";
		realProperty = null;
		askingParam = null;
		responce = new Responce();
	}
	
	//展示目前对话管理器的内容
	public String showDetail() {
		if (realProperty==null){
			return "识别对象失败！";
		}
		String result = "";
		result += "识别到对象："+realProperty.name+'\n';
		RealProperty rp = realProperty.realproperty;
		while (rp!=null){
			result += "识别下级属性："+rp.name+'\n';
			rp = rp.realproperty;
		}
		return result;
	}
	
	//以list形式，返回所有realproperty
	public ArrayList<RealProperty> getAllProperty() {
		ArrayList<RealProperty> rp = new ArrayList<RealProperty>();
		RealProperty r = null;
		if (realProperty==null)return rp;//无对象，返回
		if (realProperty.realproperty==null)return rp;//对象无一级属性，返回
		else r = realProperty.realproperty;
		//逐层向下搜索realproperty并存入rp
		while (r!=null){
			rp.add(r);
			r = r.realproperty;
		}
		return rp;
	}
}

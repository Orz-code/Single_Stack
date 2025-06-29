import numpy as np
from keys import Cols

class Simulation_Platform:
    def __init__(self, awe_dynamic_model, awe_state_df, controller, time_step, total_time):
        self.awe_dynamic_model = awe_dynamic_model  # 电解槽模型
        self.controller = controller  # 控制器模型
        self.time_step = time_step  # 每个时间步的长度
        self.total_time = total_time  # 总仿真时间
        self.current_data = []  # 存储电流数据
        self.lye_flow_history = [] # 存储碱液流量数据
        self.temp_out_history = []  # 存储出口温度变化记录
        self.awe_state_df = awe_state_df

    def load_current_data(self, current_data):
        """
        加载输入电流数据

        Args:
            current_data (_type_): 电流数据
        """
    
        self.current_data = current_data

    def run_simulation(self):
        """
        运行仿真，并实时更新电解槽状态
        """

        num_steps = int(self.total_time / self.time_step)
        
        for step in range(num_steps):
            if step < len(self.current_data):
                current_density = self.current_data[step]
            else:
                current_density = 0  # 如果没有更多的电流数据，默认电流为0
            
            # 更新电解槽温度
            lye_flow = self.controller.lye_flow_update(current_density, self.electrolyzer.Temperature)
            self.lye_flow_history.append(lye_flow)
            temp_out_next = self.awe_dynamic_model.temp_out_next_cal(self.awe_state_df)
            self.temp_out_history.append(temp_out_next)

            # 新增一行数据（索引自动递增）
            new_row = {
                Cols.current_density: 15,
                Cols.lye_flow: 62,
                Cols.temp_environment: 15,
                Cols.lye_temp: 15,
                Cols.temp_out: 15,
                Cols.pressure: 15
            }
            self.awe_state_df.loc[len(self.awe_state_df)] = new_row  # 索引设为当前长度，自动递增
        
        print("Simulation completed.")
    
    def get_results(self):
        """获取仿真结果，包括温度变化历史

        Returns:
            numpy.array: 出口温度变化过程数据
        """

        return np.array(self.temp_out_history)
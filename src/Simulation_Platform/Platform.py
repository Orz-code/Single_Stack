import numpy as np
import pandas as pd
from keys import Cols

import matplotlib.pyplot as plt

class Simulation_Platform:
    def __init__(self,awe_static_model, awe_dynamic_model, awe_state_df, controller, time_step, total_time):
        self.awe_static_model = awe_static_model  # 电解槽稳态模型，搜寻电解最优工况
        self.awe_dynamic_model = awe_dynamic_model  # 电解槽动态模型，仿真电解槽实时状态
        self.awe_state_df = awe_state_df  # 存储电解槽状态的dataframe,已有20s电解槽运行状态
        self.controller = controller  # 控制器模型
        self.time_step = time_step  # 每个时间步的长度
        self.total_time = total_time  # 总仿真时间
        self.current_data = []  # 存储电流数据


    def load_current_data(self, current_data):
        """
        加载输入电流数据

        Args:
            current_data (_type_): 电流数据
        """
    
        self.current_data = current_data
        self.awe_state_df[Cols.current_density] =  current_data[Cols.current] / self.awe_static_model.Area_Electrode

    def run_simulation(self):
        """
        运行仿真，并实时更新电解槽状态
        """

        num_steps = int(self.total_time / self.time_step)
        
        for step in range(num_steps):
            #控制器更新电解槽系统参数设置
            lye_flow_cal, lye_temp_target= self.controller.lye_flow_update(self.awe_state_df[Cols.current_density].iloc[-1], self.awe_state_df.Temperature)
            #更新电解系统状态参数设定
            # 假设df已有数据
            new_rows = pd.DataFrame({
            Cols.lye_flow: [lye_flow_cal] * self.time_step,
            Cols.lye_temp: [lye_temp_target] * self.time_step
            })
            self.awe_state_df = pd.concat([self.awe_state_df, new_rows], ignore_index=True)
            # 更新此次仿真时间步内电解槽状态
            for time in range(self.time_step):
                voltage_next, temp_out_next = self.awe_dynamic_model.awe_state_next_cal(self.awe_state_df)
                # 获取当前最后一行的下一个索引位置
                # 在新索引位置添加值
                self.awe_state_df.loc[-10 + time] = {Cols.voltage: voltage_next, Cols.temp_out: temp_out_next}
        
        print("Simulation completed.")

    def plot_result(self):
        plt.plot(self.awe_state_df)
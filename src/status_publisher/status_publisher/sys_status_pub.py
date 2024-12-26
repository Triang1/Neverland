import rclpy
from status_interfaces.msg import SystemStatus
from rclpy.node import Node
import psutil
import platform

class SysStatusPub(Node):
    def __init__(self,node_name):
        super().__init__(node_name)
        self.status_pub = self.create_publisher(SystemStatus, 'sys_status', 10)
        self.timer_ = self.create_timer(1, self.timer_callback)
    
    def timer_callback(self):
        cpu_percent = psutil.cpu_percent()
        memory_info = psutil.virtual_memory()
        net_io_counters = psutil.net_io_counters()

        """
        builtin_interfaces/Time stamp # 记录时间戳
        string host_name # 记录主机名
        float32 cpu_percent # 记录cpu使用率
        float32 memory_percent # 记录内存使用率
        float32 memory_total # 记录内存总量
        float32 memory_available # 记录内存可用量
        float64 net_sent # 记录网络发送量 1MB=8Mb
        float64 net_recv # 记录网络接收量 
        """
        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.host_name = platform.node()
        msg.cpu_percent = cpu_percent
        msg.memory_percent = memory_info.percent
        msg.memory_total = memory_info.total/1024/1024
        msg.memory_available = memory_info.available/1024/1024
        msg.net_sent = net_io_counters.bytes_sent/1024/1024
        msg.net_recv = net_io_counters.bytes_recv/1024/1024

        self.get_logger().info(f'发布：{str(msg)}')
        self.status_pub.publish(msg)

def main():
    rclpy.init()
    node = SysStatusPub('sys_status_pub')
    rclpy.spin(node)
    rclpy.shutdown()
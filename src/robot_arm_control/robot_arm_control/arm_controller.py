# Archivo de nodo básico de prueba para verificar la comunicación con los servomotores. 
# Esto será un nodo simple que permita enviar comandos de posición a cada servo individualmente.

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray, String
import time

# Para probar sin hardware inicialmente, comentamos la importación real
# import pigpio

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        
        # Configuración de los servos (ajustar según tu hardware)
        self.servo_pins = [17, 18, 19, 20, 21, 22]  # Pines GPIO para los 6 servos
        self.servo_positions = [1500] * 6  # Posición inicial (pulsos PWM)
        
        # En una implementación completa, inicializarías pigpio aquí
        # self.pi = pigpio.pi()
        # if not self.pi.connected:
        #     self.get_logger().error('No se pudo conectar con el daemon de pigpio')
        #     return
        
        # Suscriptor para comandos de posición
        self.subscription = self.create_subscription(
            Float32MultiArray,
            'arm_positions',
            self.position_callback,
            10)
            
        # Suscriptor para comandos simples
        self.cmd_subscription = self.create_subscription(
            String,
            'arm_command',
            self.command_callback,
            10)
            
        # Simulamos movimiento y actualización
        self.timer = self.create_timer(1.0, self.status_update)
        
        self.get_logger().info('Controlador básico del brazo iniciado')
        self.get_logger().info('Usa el topic arm_positions para enviar posiciones a los servos')
        self.get_logger().info('Usa el topic arm_command con "home" para posición inicial')
    
    def position_callback(self, msg):
        """Callback para comandos de posición directa de los servos"""
        if len(msg.data) > 0:
            # Actualizar posiciones de servos que se indican
            for i, position in enumerate(msg.data):
                if i < len(self.servo_positions):
                    self.servo_positions[i] = position
                    
                    # En implementación real:
                    # self.pi.set_servo_pulsewidth(self.servo_pins[i], position)
            
            self.get_logger().info(f'Posiciones actualizadas: {self.servo_positions}')
    
    def command_callback(self, msg):
        """Callback para comandos predefinidos"""
        command = msg.data.lower()
        
        if command == "home":
            # Posición de reposo
            self.servo_positions = [1500, 1500, 1500, 1500, 1500, 1500]
            self.get_logger().info('Moviendo a posición HOME')
            
            # En implementación real:
            # for i, pin in enumerate(self.servo_pins):
            #     self.pi.set_servo_pulsewidth(pin, self.servo_positions[i])
        
        elif command == "test":
            # Secuencia de prueba
            self.get_logger().info('Ejecutando secuencia de prueba')
            # Aquí implementarías una secuencia para probar cada servo
    
    def status_update(self):
        """Publica periódicamente el estado del brazo (simulado)"""
        self.get_logger().info(f'Estado actual del brazo: {self.servo_positions}')

def main(args=None):
    rclpy.init(args=args)
    arm_controller = ArmController()
    rclpy.spin(arm_controller)
    arm_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
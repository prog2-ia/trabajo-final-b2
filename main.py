from src.modelos import Cliente # importamos los demas archivos
from src.servicios import GestorFacturacion # importamos los demas archivos

def main():
    # Instanciación de objetos [15]
    gestor = GestorFacturacion()
    
    juan = Cliente("C001", "Juan Pérez", "juan@mail.com")
    juan.saldo = 50.0  # Uso de setter [7]
    
    gestor.registrar_cliente(juan)
    
    factura = gestor.emitir_factura(101, juan)
    factura.agregar_item("Servicio Web", 500.0)
    
    gestor.mostrar_reporte()

if __name__ == "__main__":
    main()

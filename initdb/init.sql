CREATE TABLE IF NOT EXISTS habitacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL,
    planta INT NOT NULL
);

CREATE TABLE IF NOT EXISTS cama (
    codigo VARCHAR(10) PRIMARY KEY,
    id_habitacion INT NOT NULL,
    lampara BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS asistente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_acceso VARCHAR(10) UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS llamada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora_llamada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    codigo_cama VARCHAR(10) NOT NULL,
    estado BOOLEAN  NOT NULL DEFAULT 0,
    receip_id VARCHAR(50),
    FOREIGN KEY (codigo_cama) REFERENCES cama(codigo) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS presencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora_llegada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_llamada INT UNIQUE NOT NULL,
    id_asistente INT NOT NULL,
    FOREIGN KEY (id_llamada) REFERENCES llamada(id) ON DELETE CASCADE,
    FOREIGN KEY (id_asistente) REFERENCES asistente(id) ON DELETE CASCADE
);


DELIMITER $$
CREATE TRIGGER encender_lampara
AFTER INSERT ON llamada
FOR EACH ROW
BEGIN
    UPDATE cama
    SET lampara = 1
    WHERE codigo = NEW.codigo_cama;
END $$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER apagar_lampara
AFTER UPDATE ON llamada
FOR EACH ROW
BEGIN
    IF NEW.estado = 1 AND OLD.estado = 0 THEN
        UPDATE cama
        SET lampara = 0
        WHERE codigo = NEW.codigo_cama;
    END IF;
END $$
DELIMITER ;
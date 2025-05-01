CREATE TABLE IF NOT EXISTS habitacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL,
    planta INT NOT NULL
);

CREATE TABLE IF NOT EXISTS cama (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo CHAR(1) NOT NULL,
    id_habitacion INT NOT NULL,
    lampara BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (id_habitacion) REFERENCES habitacion(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS asistente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_acceso VARCHAR(6) UNIQUE NOT NULL
);


CREATE TABLE IF NOT EXISTS llamada (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hora_llamada TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    id_cama INT NOT NULL,
    estado ENUM('solicitar', 'aceptada', 'finalizada') NOT NULL DEFAULT 'solicitar',
    id_asistente INT,
    hora_atendida TIMESTAMP,
    FOREIGN KEY (id_cama) REFERENCES cama(id) ON DELETE CASCADE,
    FOREIGN KEY (id_asistente) REFERENCES asistente(id) ON DELETE CASCADE
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

CREATE TRIGGER actualizar_estado_llamada
AFTER INSERT ON presencia
FOR EACH ROW
BEGIN
    UPDATE llamada
    SET estado = 'finalizada'
    WHERE id = NEW.id_llamada;
END $$

DELIMITER ;


-- insertar base de datos cama values

-- ...existing code...

-- Inserción de habitaciones
INSERT INTO habitacion (numero, planta) VALUES
(100, 1), (101, 1), (102, 1), (103, 1), (104, 1), (105, 1), (106, 1), (107, 1), (108, 1), (109, 1),
(200, 2), (201, 2), (202, 2), (203, 2), (204, 2), (205, 2), (206, 2), (207, 2), (208, 2), (209, 2),
(300, 3), (301, 3), (302, 3), (303, 3), (304, 3), (305, 3), (306, 3), (307, 3), (308, 3), (309, 3),
(400, 4), (401, 4), (402, 4), (403, 4), (404, 4), (405, 4), (406, 4), (407, 4), (408, 4), (409, 4),
(500, 5), (501, 5), (502, 5), (503, 5), (504, 5), (505, 5), (506, 5), (507, 5), (508, 5), (509, 5);

-- Inserción de camas
INSERT INTO cama (codigo, id_habitacion, lampara) VALUES
('A', 1, 0), ('B', 1, 0),
('A', 2, 0), ('B', 2, 0),
('A', 3, 0), ('B', 3, 0),
('A', 4, 0), ('B', 4, 0),
('A', 5, 0), ('B', 5, 0),
('A', 6, 0), ('B', 6, 0),
('A', 7, 0), ('B', 7, 0),
('A', 8, 0), ('B', 8, 0),
('A', 9, 0), ('B', 9, 0),
('A', 10, 0), ('B', 10, 0),
('A', 11, 0), ('B', 11, 0),
('A', 12, 0), ('B', 12, 0),
('A', 13, 0), ('B', 13, 0),
('A', 14, 0), ('B', 14, 0),
('A', 15, 0), ('B', 15, 0),
('A', 16, 0), ('B', 16, 0),
('A', 17, 0), ('B', 17, 0),
('A', 18, 0), ('B', 18, 0),
('A', 19, 0), ('B', 19, 0),
('A', 20, 0), ('B', 20, 0),
('A', 21, 0), ('B', 21, 0),
('A', 22, 0), ('B', 22, 0),
('A', 23, 0), ('B', 23, 0),
('A', 24, 0), ('B', 24, 0),
('A', 25, 0), ('B', 25, 0),
('A', 26, 0), ('B', 26, 0),
('A', 27, 0), ('B', 27, 0),
('A', 28, 0), ('B', 28, 0),
('A', 29, 0), ('B', 29, 0),
('A', 30, 0), ('B', 30, 0),
('A', 31, 0), ('B', 31, 0),
('A', 32, 0), ('B', 32, 0),
('A', 33, 0), ('B', 33, 0),
('A', 34, 0), ('B', 34, 0),
('A', 35, 0), ('B', 35, 0),
('A', 36, 0), ('B', 36, 0),
('A', 37, 0), ('B', 37, 0),
('A', 38, 0), ('B', 38, 0),
('A', 39, 0), ('B', 39, 0),
('A', 40, 0), ('B', 40, 0),
('A', 41, 0), ('B', 41, 0),
('A', 42, 0), ('B', 42, 0),
('A', 43, 0), ('B', 43, 0),
('A', 44, 0), ('B', 44, 0),
('A', 45, 0), ('B', 45, 0),
('A', 46, 0), ('B', 46, 0),
('A', 47, 0), ('B', 47, 0),
('A', 48, 0), ('B', 48, 0),
('A', 49, 0), ('B', 49, 0),
('A', 50, 0), ('B', 50, 0);


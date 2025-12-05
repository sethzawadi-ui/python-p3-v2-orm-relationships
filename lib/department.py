from __init__ import CONN, CURSOR

class Department:
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location
        if self.id:
            Department.all[self.id] = self

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments"
        CURSOR.execute(sql)
        CONN.commit()
        cls.all = {}

    def save(self):
        if self.id is None:
            sql = "INSERT INTO departments (name, location) VALUES (?, ?)"
            CURSOR.execute(sql, (self.name, self.location))
            CONN.commit()
            self.id = CURSOR.lastrowid
            Department.all[self.id] = self
        else:
            self.update()

    @classmethod
    def create(cls, name, location):
        dep = cls(name, location)
        dep.save()
        return dep

    def update(self):
        sql = "UPDATE departments SET name=?, location=? WHERE id=?"
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM departments WHERE id=?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        Department.all.pop(self.id, None)
        self.id = None

    @classmethod
    def instance_from_db(cls, row):
        return cls(row[1], row[2], row[0])

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM departments"
        rows = CURSOR.execute(sql).fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        if id in cls.all:
            return cls.all[id]
        sql = "SELECT * FROM departments WHERE id=?"
        row = CURSOR.execute(sql, (id,)).fetchone()
        if row:
            dep = cls.instance_from_db(row)
            cls.all[dep.id] = dep
            return dep
        return None

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM departments WHERE name=?"
        row = CURSOR.execute(sql, (name,)).fetchone()
        if row:
            dep = cls.instance_from_db(row)
            cls.all[dep.id] = dep
            return dep
        return None

    def employees(self):
        from employee import Employee
        return [emp for emp in Employee.get_all() if emp.department_id == self.id]

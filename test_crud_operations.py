import pytest
from sqlalchemy.orm import Session
from database import get_db, Student, Subject, create_tables, SessionLocal
from datetime import datetime

# Фикстура для тестовой сессии БД
@pytest.fixture(scope="function")
def db_session():
    # Создаем таблицы если их нет
    create_tables()
    
    # Создаем новую сессию
    db = SessionLocal()
    try:
        yield db
    finally:
        # Очищаем тестовые данные после каждого теста
        db.query(Student).filter(Student.email.like("%test%")).delete()
        db.query(Subject).filter(Subject.name.like("%Test%")).delete()
        db.commit()
        db.close()

class TestCRUDOperations:
    
    def test_create_student(self, db_session: Session):
        """Тест на создание студента"""
        # Создаем тестового студента
        new_student = Student(
            name="Test Student",
            email="test.student@example.com"
        )
        
        db_session.add(new_student)
        db_session.commit()
        db_session.refresh(new_student)
        
        # Проверяем, что студент создан
        student_from_db = db_session.query(Student).filter(
            Student.email == "test.student@example.com"
        ).first()
        
        assert student_from_db is not None
        assert student_from_db.name == "Test Student"
        assert student_from_db.email == "test.student@example.com"
        assert student_from_db.is_active == True
        assert student_from_db.deleted_at is None
    
    def test_update_student(self, db_session: Session):
        """Тест на обновление студента"""
        # Сначала создаем студента
        student = Student(
            name="Test Student Update",
            email="test.update@example.com"
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        
        # Обновляем студента
        student_id = student.id
        db_session.query(Student).filter(Student.id == student_id).update({
            "name": "Updated Test Student",
            "email": "updated.test@example.com"
        })
        db_session.commit()
        
        # Проверяем обновление
        updated_student = db_session.query(Student).filter(Student.id == student_id).first()
        
        assert updated_student is not None
        assert updated_student.name == "Updated Test Student"
        assert updated_student.email == "updated.test@example.com"
    
    def test_soft_delete_student(self, db_session: Session):
        """Тест на мягкое удаление студента"""
        # Создаем студента для удаления
        student = Student(
            name="Test Student Delete",
            email="test.delete@example.com"
        )
        db_session.add(student)
        db_session.commit()
        db_session.refresh(student)
        
        student_id = student.id
        
        # Выполняем мягкое удаление
        db_session.query(Student).filter(Student.id == student_id).update({
            "deleted_at": datetime.utcnow(),
            "is_active": False
        })
        db_session.commit()
        
        # Проверяем, что студент "удален" (soft delete)
        deleted_student = db_session.query(Student).filter(Student.id == student_id).first()
        
        assert deleted_student is not None
        assert deleted_student.deleted_at is not None
        assert deleted_student.is_active == False
        
        # Проверяем, что студент не находится в обычных запросах
        active_students = db_session.query(Student).filter(
            Student.deleted_at.is_(None)
        ).all()
        
        student_in_active = any(s.id == student_id for s in active_students)
        assert not student_in_active, "Студент не должен быть в списке активных после soft delete"

class TestSubjectCRUD:
    
    def test_create_subject(self, db_session: Session):
        """Тест на создание предмета"""
        new_subject = Subject(
            name="Test Subject",
            description="This is a test subject for testing purposes"
        )
        
        db_session.add(new_subject)
        db_session.commit()
        db_session.refresh(new_subject)
        
        # Проверяем создание предмета
        subject_from_db = db_session.query(Subject).filter(
            Subject.name == "Test Subject"
        ).first()
        
        assert subject_from_db is not None
        assert subject_from_db.name == "Test Subject"
        assert subject_from_db.description == "This is a test subject for testing purposes"
        assert subject_from_db.is_active == True
        assert subject_from_db.deleted_at is None

# Дополнительные тесты для демонстрации стабильности
class TestStability:
    
    def test_idempotent_creation(self, db_session: Session):
        """Тест на идемпотентность создания"""
        # Этот тест можно запускать многократно с одинаковым результатом
        email = "stable.test@example.com"
        
        # Удаляем если существует (для чистоты теста)
        db_session.query(Student).filter(Student.email == email).delete()
        db_session.commit()
        
        # Создаем студента
        student = Student(name="Stable Test", email=email)
        db_session.add(student)
        db_session.commit()
        
        # Проверяем создание
        created = db_session.query(Student).filter(Student.email == email).first()
        assert created is not None
        assert created.email == email
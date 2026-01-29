# 📌 Aplikacja do zarządzania zadaniami i notatkami

## Opis projektu

Projekt jest aplikacją webową do zarządzania zadaniami (tasks) oraz notatkami (notes), tworzonymi w ramach list zadań (tasklists), które należą do grup użytkowników (groups).

Aplikacja umożliwia:
- tworzenie i zarządzanie grupami użytkowników,
- przypisywanie użytkowników do grup,
- tworzenie list zadań w ramach grup,
- tworzenie zadań i notatek w ramach list,
- zarządzanie statusem, priorytetem i treścią zadań,
- kontrolę dostępu opartą o role (lider grupy / członek).

Projekt jest realizowany jako **backend API**, przeznaczony do współpracy z aplikacją frontendową (np. SPA).

---

## Główne założenia funkcjonalne

### Grupy (Groups)
- Każda grupa ma lidera (creatora).
- Lider może:
  - dodawać i usuwać członków,
  - zmieniać nazwę grupy,
  - tworzyć listy zadań.
- Członkowie mogą pracować tylko w grupach, do których należą.

### Listy zadań (TaskLists)
- TaskList zawsze należy do jednej grupy.
- W ramach listy można:
  - tworzyć zadania,
  - tworzyć notatki.

### Zadania (Tasks)
- Zadanie ma:
  - wykonawcę (performer),
  - status (`open`, `submitted`, `accepted`, `rejected`),
  - priorytet,
  - tytuł.
- Status zadania może być zmieniany zgodnie z regułami biznesowymi.
- Zadania są zawsze przypisane do konkretnej listy zadań.

### Notatki (Notes)
- Notatki należą do listy zadań.
- Mają autora, tytuł i treść.
- Mogą być filtrowane po wykonawcy.

---

## Autoryzacja i bezpieczeństwo

- API korzysta z **Django authentication**.
- Każde żądanie wymaga uwierzytelnionego użytkownika.
- Uprawnienia są sprawdzane na poziomie logiki aplikacyjnej (use cases), np.:
  - czy użytkownik należy do grupy,
  - czy jest liderem grupy,
  - czy może wykonać daną akcję na zasobie.

---

## Architektura aplikacji

Projekt wykorzystuje **architekturę warstwową**, oddzielając odpowiedzialności poszczególnych elementów systemu.

### Warstwy systemu

```

┌────────────────────┐
│  API (Django Ninja)│
└─────────▲──────────┘
│
┌─────────┴──────────┐
│ Application Layer  │  ← Use cases / Services
└─────────▲──────────┘
│
┌─────────┴──────────┐
│ Domain Layer       │  ← Encje, logika domenowa
└─────────▲──────────┘
│
┌─────────┴──────────┐
│ Infrastructure     │  ← Django ORM, Repositories
└────────────────────┘

````

---

## API Layer (Django Ninja)

- Odpowiada wyłącznie za:
  - obsługę HTTP,
  - walidację danych wejściowych (schemas),
  - serializację odpowiedzi.
- Nie zawiera logiki biznesowej.
- Każdy endpoint deleguje pracę do odpowiedniego **use case**.

Przykład:
```python
@api.patch('/task/{task_id}/{action}')
def change_task_status(request, task_id, action):
    ChangeTaskStatus().execute(...)
````

---

## Application Layer (Use Cases)

* Każda operacja biznesowa jest reprezentowana przez osobny use case.
* Use case:

  * pobiera dane z repozytoriów,
  * sprawdza uprawnienia,
  * wykonuje logikę biznesową,
  * zapisuje zmiany.

Przykłady:

* `CreateTask`
* `ChangeTaskStatus`
* `GetTasksByTasklist`
* `AddNewMemberGroup`

Use case **nie zależy od frameworka webowego**.

---

## Domain Layer

* Zawiera encje domenowe (np. Task, Group).
* Encje implementują reguły biznesowe, np.:

  * zmiana statusu zadania,
  * walidacja dozwolonych akcji.
* Logika domenowa jest niezależna od bazy danych i API.

---

## Repositories (Infrastructure Layer)

* Repozytoria odpowiadają za:

  * mapowanie encji domenowych na modele Django ORM,
  * zapisy i odczyty z bazy danych.
* Dzięki repozytoriom:

  * use cases nie znają ORM,
  * logika aplikacji jest testowalna.

Przykład:

```python
TaskRepository.get(task_id)
TaskRepository.save(task)
```

---

## Styl API

API nie jest w pełni REST-owe w klasycznym znaczeniu.

Charakterystyka:

* endpointy są **operacyjne (command-based)**,
* skupione na akcjach, np.:

  * `/task/{id}/submit`
  * `/task/{id}/accept`

To podejście upraszcza implementację reguł biznesowych i jest świadomym kompromisem projektowym.

---

## Testy

Projekt zawiera:

* testy jednostkowe logiki aplikacyjnej,
* testy repozytoriów,
* testy API (pytest + Ninja TestClient).

Testy:

* sprawdzają poprawność reguł biznesowych,
* zabezpieczają przed regresją,
* umożliwiają bezpieczny rozwój projektu.

---


## Technologie

* Python
* Django
* Django Ninja
* Django ORM
* Pytest





## Wzorce projektowe (GoF) użyte w projekcie

Projekt wykorzystuje kilka klasycznych wzorców projektowych (Gang of Four),
świadomie lub naturalnie wynikających z przyjętej architektury warstwowej.

---

### 1. **Repository**

**Cel:**  
Oddzielenie logiki domenowej i aplikacyjnej od sposobu dostępu do danych.

**Gdzie używany:**
- `TaskRepository`
- `GroupRepository`
- `TaskListRepository`
- `NoteRepository`

**Opis:**
Repozytoria zapewniają jednolity interfejs do operacji na danych
(pobieranie, zapisywanie), ukrywając szczegóły Django ORM.

Use case nie zna:
- modeli Django,
- zapytań SQL,
- struktury bazy danych.

**Przykład:**
```python
task = task_rep.get(task_id)
task_rep.save(task)


**Korzyści:**

* łatwiejsze testowanie,
* mniejsza zależność od frameworka,
* możliwość zmiany warstwy persystencji.
```
---

### 2. **Command**

**Cel:**
Hermetyzacja pojedynczej operacji biznesowej w osobnym obiekcie.

**Gdzie używany:**
Każdy use case jest komendą:

* `CreateTask`
* `ChangeTaskStatus`
* `AddNewMemberGroup`
* `CreateNote`

**Opis:**
Każdy use case:

* posiada metodę `execute`,
* reprezentuje jedną akcję systemu,
* może być testowany niezależnie.

**Przykład:**

```python
ChangeTaskStatus().execute(...)
```

**Korzyści:**

* czytelna struktura aplikacji,
* łatwe rozszerzanie funkcjonalności,
* brak „fat controllers”.

---

### 3. **Facade**

**Cel:**
Uproszczenie interfejsu dostępu do złożonej logiki.

**Gdzie używany:**

* warstwa API (Django Ninja)

**Opis:**
Endpoint API działa jako fasada:

* zbiera dane z requestu,
* deleguje logikę do use case,
* zwraca odpowiedź HTTP.

API **nie zawiera logiki biznesowej**.

**Przykład:**

```python
@api.post(...)
def create_task(...):
    CreateTask().execute(...)
```

---


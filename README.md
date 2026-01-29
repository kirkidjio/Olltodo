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

# Dokumentacja kodu


Dokumentacja skupia się wyłącznie na **implementacji**,
bez teoretycznych rozważań.

---

## Warstwy aplikacji

Projekt podzielony jest na cztery główne warstwy:

1. **Domain** – logika biznesowa i reguły
2. **Application / Service** – przypadki użycia (use cases)
3. **Repositories** – dostęp do danych
4. **API** – komunikacja HTTP (Django Ninja)

---

## 1. Warstwa domeny (`core/domain`)

### Cel
Warstwa domeny zawiera:
- encje biznesowe,
- reguły,
- walidację,
- zmiany stanu.

Domena **nie zna**:
- frameworków,
- Django,
- bazy danych,
- HTTP.

---

### Encja `Group`

**Plik:** `core/domain/entities/group.py`

**Odpowiedzialność:**
- przechowywanie informacji o grupie,
- kontrola uprawnień lidera,
- zarządzanie członkami.

**Najważniejsze pola:**
- `id`
- `leader`
- `members`
- `name`

**Najważniejsze metody:**
- `add(actor_id, member_id)` – dodanie członka
- `rem(actor_id, member_id)` – usunięcie członka
- `change_name(actor_id, name)` – zmiana nazwy

**Reguły:**
- tylko lider może zmieniać grupę,
- członkowie są unikalni.

---

### Encja `Task`

**Plik:** `core/domain/entities/task.py`

**Odpowiedzialność:**
- przechowywanie stanu zadania,
- kontrola przejść statusów,
- walidacja akcji użytkownika.

**Najważniejsze pola:**
- `id`
- `checker` (lider)
- `performer`
- `status`
- `priority`
- `title`

**Metody zmiany stanu:**
- `submit(actor_id)`
- `accept(actor_id)`
- `reject(actor_id)`

**Reguły:**
- performer może `submit`,
- lider może `accept` / `reject`,
- niedozwolone przejścia rzucają wyjątek.

---

### Encja `TaskList`

**Plik:** `core/domain/models/tasklist.py`

**Odpowiedzialność:**
- reprezentowanie listy zadań,
- powiązanie z grupą.

**Pola:**
- `id`
- `name`
- `group_id`

TaskList **nie zawiera logiki zadań** – służy jako kontekst.

---

### Encja `Note`

**Plik:** `core/domain/entities/note.py`

**Odpowiedzialność:**
- przechowywanie notatek,
- kontrola edycji przez autora.

**Reguły:**
- tylko autor może edytować treść i tytuł.

---

## 2. Warstwa aplikacji / serwisów (`core/application/service`)

### Cel
Warstwa service:
- realizuje konkretne przypadki użycia,
- orkiestruje encje i repozytoria,
- sprawdza uprawnienia między obiektami.

Service **nie przechowuje stanu**.

---

### Zasada ogólna

Każdy use case:
- jest jedną klasą,
- ma metodę `execute(...)`,
- wykonuje **jedną akcję biznesową**.

---

### Task services (`tasks.py`)

#### `CreateTask`

- sprawdza istnienie tasklisty,
- pobiera grupę,
- sprawdza czy actor jest liderem,
- sprawdza czy performer jest członkiem,
- tworzy zadanie.

---

#### `ChangeTaskStatus`

- pobiera zadanie,
- wywołuje odpowiednią metodę domenową (`submit/accept/reject`),
- zapisuje zmiany.

Logika przejść **jest w domenie**, nie w serwisie.

---

#### `ChangeTaskPriority`
#### `ChangeTaskTitle`

- pobierają zadanie,
- delegują walidację do encji,
- zapisują wynik.

---

### Group services (`groups.py`)

- `CreateGroup`
- `AddNewMemberGroup`
- `RemoveMemberGroup`
- `ChangeNameGroup`

Każdy serwis:
- pobiera grupę,
- wywołuje metodę encji,
- zapisuje zmiany.

---

### TaskList services (`tasklist.py`)

- `CreateTaskList`
- sprawdza czy actor jest liderem grupy,
- tworzy listę zadań przypisaną do grupy.

---

### Note services (`notes.py`)

- `CreateNote`
- `ChangeTitleNote`
- `ChangeContentNote`
- `GetNotesByPerformer`

Serwisy notatek:
- sprawdzają przynależność do grupy,
- delegują walidację do encji `Note`.

---

## 3. Repozytoria (`core/repositories`)

### Cel
Repozytoria:
- mapują Django ORM → encje domenowe,
- zapisują zmiany do bazy,
- ukrywają szczegóły persystencji.

---

### Zasady

- repozytorium **nie zawiera logiki biznesowej**,
- tylko CRUD + mapowanie,
- encje domenowe nie znają ORM.

---

### Przykład: `TaskRepository`

**Odpowiedzialność:**
- pobieranie zadań z bazy,
- mapowanie na encję `Task`,
- zapisywanie zmian.

**Metody:**
- `get(id)`
- `get_by_tasklist(tasklist_id)`
- `get_in_tasklist_by_performer(...)`
- `save(task, tasklist_id=None)`

---

## 4. Warstwa API (`core/api`)

### Cel
API:
- odbiera request HTTP,
- waliduje dane wejściowe (Schema),
- wywołuje use case,
- zwraca odpowiedź.

API **nie zawiera logiki biznesowej**.

---

### Django Ninja

- używane są `Schema` jako DTO,
- autoryzacja przez `django_auth`,
- odpowiedzi JSON.

---

### Przykład endpointu

```python
@api.patch('/task/{task_id}/{action}')
def change_task_status(request, task_id, action):
    ChangeTaskStatus().execute(
        task_id=task_id,
        actor_id=request.user.id,
        action=action,
        task_rep=TaskRepository()
    )



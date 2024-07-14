import 'package:mobile/models.dart';
import 'package:path/path.dart' as path;
import 'package:sqflite/sqflite.dart' as sql;
import 'package:sqflite/sqlite_api.dart';
import 'package:riverpod_annotation/riverpod_annotation.dart';

part 'tasks_provider.g.dart';

Future<Database> _getDatabase() async {
  final dbPath = await sql.getDatabasesPath();
  final db = await sql.openDatabase(path.join(dbPath, 'stickydo.db'),
      onCreate: (db, version) {
    return db.execute("""
        CREATE TABLE task (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        priority INTEGER NOT NULL,
        text TEXT NOT NULL,
        completed BOOLEAN NOT NULL DEFAULT 0,
        created_at DATE NOT NULL);
    """);
  }, version: 1);

  return db;
}

@riverpod
class AsyncTask extends _$AsyncTask {
  @override
  FutureOr<List<Task>> build(String createdAt) async {
    return _fetchTasks(createdAt: createdAt);
  }

  Future<List<Task>> _fetchTasks({required String createdAt}) async {
    final db = await _getDatabase();

    // Fetch tasks where created_at is equal to the provided createdAt date
    final List<Map<String, dynamic>> data = await db.query(
      'task',
      where: 'DATE(created_at) = ?',
      whereArgs: [createdAt],
    );

    final tasks = data
        .map(
          (row) => Task(
              id: row["id"],
              priority: row['priority'],
              text: row['text'] as String,
              completed: row['completed'] == 0 ? false : true,
              createdAt: row['created_at']),
        )
        .toList();

    return tasks;
  }

  Future<void> addTask(Task task) async {
    // Set the state to loading
    state = const AsyncValue.loading();
    // Add the new todo and reload the todo list from the remote repository
    state = await AsyncValue.guard(() async {
      final db = await _getDatabase();
      db.insert('task', {
        'priority': task.priority,
        'text': task.text,
        'created_at': task.createdAt,
      });

      return _fetchTasks(createdAt: '2024-07-14');
    });
  }

  Future<void> removeTask(int taskID) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final db = await _getDatabase();
      await db.delete('task', where: 'id = ?', whereArgs: [taskID]);
      return _fetchTasks(createdAt: '2024-07-14');
    });
  }

  Future<void> toggleTaskComplete(int taskID, bool newCompleted) async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() async {
      final db = await _getDatabase();
      await db.update('task', {'completed': newCompleted},
          where: 'id = ?', whereArgs: [taskID]);
      return _fetchTasks(createdAt: '2024-07-14');
    });
  }
}

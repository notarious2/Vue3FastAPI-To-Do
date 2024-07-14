class Task {
  final int? id;
  final int priority;
  final String text;
  final bool completed;
  final String createdAt;

  Task({
    this.id,
    required this.priority,
    required this.text,
    required this.completed,
    required this.createdAt,
  });

  Task copyWith({
    int? id,
    int? priority,
    String? text,
    bool? completed,
    String? createdAt,
  }) {
    return Task(
      id: id ?? this.id,
      priority: priority ?? this.priority,
      text: text ?? this.text,
      completed: completed ?? this.completed,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}

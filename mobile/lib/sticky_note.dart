import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile/models.dart';
import 'package:mobile/sticky_note_painter.dart';
import 'package:mobile/tasks_provider.dart';

class StickyNote extends ConsumerWidget {
  const StickyNote({
    super.key,
    required this.items,
    this.color = const Color(0xffffff00),
  });

  final List<Task> items;
  final Color color;

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return Transform.rotate(
      angle: 0,
      child: CustomPaint(
        painter: StickyNotePainter(color: color),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: items.asMap().entries.map((entry) {
                final index = entry.key;
                final item = entry.value;
                return Column(
                  children: [
                    Dismissible(
                      key: Key('${item.id}'),
                      onDismissed: (direction) {
                        ref
                            .read(AsyncTaskProvider('2024-07-14').notifier)
                            .removeTask(item.id!);
                        ScaffoldMessenger.of(context).clearSnackBars();
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('${item.text} deleted')),
                        );
                      },
                      background: Container(
                        color: const Color.fromARGB(255, 210, 118, 203),
                      ),
                      child: Row(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${index + 1}. ',
                            style: const TextStyle(fontSize: 18),
                          ),
                          Expanded(
                            child: Text(
                              item.text,
                              style: const TextStyle(fontSize: 18),
                              overflow: TextOverflow.visible,
                            ),
                          ),
                          const Spacer(),
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              const Icon(Icons.edit),
                              IconButton(
                                icon: const Icon(Icons.delete),
                                onPressed: () {
                                  ref
                                      .read(AsyncTaskProvider('2024-07-14')
                                          .notifier)
                                      .removeTask(item.id!);
                                },
                              ),
                              Checkbox(
                                value: item.completed,
                                checkColor: Colors.black,
                                fillColor: WidgetStateProperty.resolveWith(
                                  (states) {
                                    if (!states
                                        .contains(WidgetState.selected)) {
                                      return const Color(0xffffff00);
                                    }
                                    return Colors.transparent;
                                  },
                                ),
                                onChanged: (bool? value) {
                                  ref
                                      .read(AsyncTaskProvider('2024-07-14')
                                          .notifier)
                                      .toggleTaskComplete(item.id!, value!);
                                },
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ],
                );
              }).toList(),
            ),
          ),
        ),
      ),
    );
  }
}

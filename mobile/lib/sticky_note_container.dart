import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mobile/tasks_provider.dart';
import 'sticky_note.dart';

class StickyNoteContainer extends ConsumerWidget {
  const StickyNoteContainer({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final asyncTasks = ref.watch(AsyncTaskProvider('2024-07-14'));

    return asyncTasks.when(
      data: (tasks) => Container(
        color: Colors.white,
        child: Center(
          child: SizedBox(
            width: 350,
            height: 350,
            child: Container(
              color: Colors.white,
              child: StickyNote(
                items: tasks,
              ),
            ),
          ),
        ),
      ),
      loading: () => const Center(child: CircularProgressIndicator()),
      error: (error, stack) => Text('Error: $error'),
    );
  }
}

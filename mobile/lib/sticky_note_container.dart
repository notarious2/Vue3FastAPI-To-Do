import 'package:flutter/material.dart';
import 'sticky_note.dart';

class StickyNoteContainer extends StatelessWidget {
  const StickyNoteContainer({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white,
      child: Center(
        child: SizedBox(
          width: 350,
          height: 350,
          child: Container(
            color: Colors.white,
            child: StickyNote(
              items: [
                'Buy groceries',
                'Call Alice',
                'Walk the dog',
                'Buy something',
                'Buy groceries',
                'Call Alice',
                'Walk the dog',
                'Buy something',
                'Buy groceries',
                'Call Alice',
                'Walk the dog',
                'Buy something',
                'Buy groceries',
                'Call Alice',
                'Walk the dog',
                'Buy something',
              ],
            ),
          ),
        ),
      ),
    );
  }
}

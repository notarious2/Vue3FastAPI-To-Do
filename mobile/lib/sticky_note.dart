import 'package:flutter/material.dart';
import 'package:mobile/sticky_note_painter.dart';

class StickyNote extends StatefulWidget {
  const StickyNote({
    super.key,
    required this.items,
    this.color = const Color(0xffffff00),
  });

  final List<String> items;
  final Color color;

  @override
  _StickyNoteState createState() => _StickyNoteState();
}

class _StickyNoteState extends State<StickyNote> {
  late List<String> items;
  bool isChecked = false;

  @override
  void initState() {
    super.initState();
    items = widget.items;
  }

  @override
  Widget build(BuildContext context) {
    return Transform.rotate(
      angle: 0,
      child: CustomPaint(
        painter: StickyNotePainter(color: widget.color),
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
                      key: Key('$item-$index'),
                      onDismissed: (direction) {
                        setState(() {
                          items.removeAt(index);
                        });
                        ScaffoldMessenger.of(context).clearSnackBars();
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('$item deleted')),
                        );
                      },
                      background:
                          Container(color: Color.fromARGB(255, 210, 118, 203)),
                      child: Row(
                        children: [
                          Text(
                            '${index + 1}. ',
                            style: const TextStyle(fontSize: 18),
                          ),
                          Text(
                            item,
                            style: const TextStyle(fontSize: 18),
                          ),
                          const Spacer(),
                          Icon(Icons.edit),
                          Icon(
                            Icons.delete,
                            color: Colors.pink,
                          ),
                          Checkbox(
                              value: isChecked,
                              onChanged: (bool? value) {
                                setState(() {
                                  isChecked = value!;
                                });
                              })
                        ],
                      ),
                    ),
                    // const SizedBox(height: 3), // Add margin here
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

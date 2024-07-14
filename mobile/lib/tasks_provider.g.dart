// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'tasks_provider.dart';

// **************************************************************************
// RiverpodGenerator
// **************************************************************************

String _$asyncTaskHash() => r'6ad023e1f15f22975c81cd2d1c4465aa57b6513b';

/// Copied from Dart SDK
class _SystemHash {
  _SystemHash._();

  static int combine(int hash, int value) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + value);
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x0007ffff & hash) << 10));
    return hash ^ (hash >> 6);
  }

  static int finish(int hash) {
    // ignore: parameter_assignments
    hash = 0x1fffffff & (hash + ((0x03ffffff & hash) << 3));
    // ignore: parameter_assignments
    hash = hash ^ (hash >> 11);
    return 0x1fffffff & (hash + ((0x00003fff & hash) << 15));
  }
}

abstract class _$AsyncTask
    extends BuildlessAutoDisposeAsyncNotifier<List<Task>> {
  late final String createdAt;

  FutureOr<List<Task>> build(
    String createdAt,
  );
}

/// See also [AsyncTask].
@ProviderFor(AsyncTask)
const asyncTaskProvider = AsyncTaskFamily();

/// See also [AsyncTask].
class AsyncTaskFamily extends Family<AsyncValue<List<Task>>> {
  /// See also [AsyncTask].
  const AsyncTaskFamily();

  /// See also [AsyncTask].
  AsyncTaskProvider call(
    String createdAt,
  ) {
    return AsyncTaskProvider(
      createdAt,
    );
  }

  @override
  AsyncTaskProvider getProviderOverride(
    covariant AsyncTaskProvider provider,
  ) {
    return call(
      provider.createdAt,
    );
  }

  static const Iterable<ProviderOrFamily>? _dependencies = null;

  @override
  Iterable<ProviderOrFamily>? get dependencies => _dependencies;

  static const Iterable<ProviderOrFamily>? _allTransitiveDependencies = null;

  @override
  Iterable<ProviderOrFamily>? get allTransitiveDependencies =>
      _allTransitiveDependencies;

  @override
  String? get name => r'asyncTaskProvider';
}

/// See also [AsyncTask].
class AsyncTaskProvider
    extends AutoDisposeAsyncNotifierProviderImpl<AsyncTask, List<Task>> {
  /// See also [AsyncTask].
  AsyncTaskProvider(
    String createdAt,
  ) : this._internal(
          () => AsyncTask()..createdAt = createdAt,
          from: asyncTaskProvider,
          name: r'asyncTaskProvider',
          debugGetCreateSourceHash:
              const bool.fromEnvironment('dart.vm.product')
                  ? null
                  : _$asyncTaskHash,
          dependencies: AsyncTaskFamily._dependencies,
          allTransitiveDependencies: AsyncTaskFamily._allTransitiveDependencies,
          createdAt: createdAt,
        );

  AsyncTaskProvider._internal(
    super._createNotifier, {
    required super.name,
    required super.dependencies,
    required super.allTransitiveDependencies,
    required super.debugGetCreateSourceHash,
    required super.from,
    required this.createdAt,
  }) : super.internal();

  final String createdAt;

  @override
  FutureOr<List<Task>> runNotifierBuild(
    covariant AsyncTask notifier,
  ) {
    return notifier.build(
      createdAt,
    );
  }

  @override
  Override overrideWith(AsyncTask Function() create) {
    return ProviderOverride(
      origin: this,
      override: AsyncTaskProvider._internal(
        () => create()..createdAt = createdAt,
        from: from,
        name: null,
        dependencies: null,
        allTransitiveDependencies: null,
        debugGetCreateSourceHash: null,
        createdAt: createdAt,
      ),
    );
  }

  @override
  AutoDisposeAsyncNotifierProviderElement<AsyncTask, List<Task>>
      createElement() {
    return _AsyncTaskProviderElement(this);
  }

  @override
  bool operator ==(Object other) {
    return other is AsyncTaskProvider && other.createdAt == createdAt;
  }

  @override
  int get hashCode {
    var hash = _SystemHash.combine(0, runtimeType.hashCode);
    hash = _SystemHash.combine(hash, createdAt.hashCode);

    return _SystemHash.finish(hash);
  }
}

mixin AsyncTaskRef on AutoDisposeAsyncNotifierProviderRef<List<Task>> {
  /// The parameter `createdAt` of this provider.
  String get createdAt;
}

class _AsyncTaskProviderElement
    extends AutoDisposeAsyncNotifierProviderElement<AsyncTask, List<Task>>
    with AsyncTaskRef {
  _AsyncTaskProviderElement(super.provider);

  @override
  String get createdAt => (origin as AsyncTaskProvider).createdAt;
}
// ignore_for_file: type=lint
// ignore_for_file: subtype_of_sealed_class, invalid_use_of_internal_member, invalid_use_of_visible_for_testing_member

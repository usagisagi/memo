# 共変性・反変性とリスコフの置換の原則 #

## モデル ##

上記の本だと継承の例として`Entity`と`User`となっていましたが、より直観的に理解するために`Float`と`Integer`で考えてみます。直観としては小数は整数を拡張した概念で、「整数は小数として扱える」けど「小数は整数として扱えない」のような感じです。2は2.0として小数として扱えるけど、2.5は整数にできない。

```CSharp
    public class TypeInteger {
        public object Value { get; private set; }
    }

    public class TypeFloat : TypeInteger {  }
```

### 共変性 ###

型パラメータに共変性を指定すると、そのパラメータの他に継承先を代入できます。戻値の型に使います。

```CSharp
public interface IIntegerCalculator<out TInteger> where TInteger : TypeInteger {
    TInteger ReturnInteger();
}

public class FloatCalculator : IIntegerCalculator<TypeFloat> {
    public TypeFloat ReturnInteger() {
        return new TypeFloat();
    }
}

public class Test {
    public void TestMethod2() {
        IIntegerCalculator<TypeInteger> integerCalculator = new FloatCalculator();
    }
}
```

### 反変性 ###

型パラメータに反変性を指定すると、そのパラメータの他に継承元を指定できます。引数の型に使います。

```CSharp
public interface IEqualityComparer<in TFloat> where TFloat : TypeInteger {
    bool Equals(TFloat left, TFloat right);
}

public class EqualityComparer : IEqualityComparer<TypeInteger> {
    public bool Equals(TypeInteger left, TypeInteger right) {
        return left.Value == right.Value;
    }
}

public class Test {
    public void TestMethod() {
        IEqualityComparer<TypeFloat> equalityComparer = new EqualityComparer();
        var float1 = new TypeFloat();
        var float2 = new TypeFloat();
        equalityComparer.Equals(user1, user2);
    }
}
```

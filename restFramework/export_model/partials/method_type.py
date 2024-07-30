'''
1) _get_method_type:
------------------------------
Bu fonksiyon, Python'daki bir sınıf yöntemi (method) nesnesinin tipini belirlemek için kullanılır.
Bu, özel metodların sınıf içinde nasıl saklandığını anlamak için faydalıdır.

2) ExampleClass:
------------------------------
ExampleClass adında basit bir sınıf tanımlanır. Bu sınıf, bir örnek metod olan example_method içerir.
Bu metod, sınıfın içindeki bir metodun tipini belirlemek için kullanılır.

3) type(ExampleClass.example_method):
------------------------------
ExampleClass sınıfındaki example_method metodunun tipini döndürür.
Bu tip, sınıf içindeki diğer metodları tanımlamak ve kontrol etmek için kullanılabilir.

4) _method_type:
------------------------------
_method_type değişkeni, ExampleClass içindeki metodların tipini saklar. Bu bilgi,
sınıf içinde metodların nasıl tanımlandığını veya değiştirildiğini kontrol etmek için kullanılabilir.
'''
def _get_method_type():
    class ExampleClass:
        def example_method(self):
            pass
    return type(ExampleClass.example_method)
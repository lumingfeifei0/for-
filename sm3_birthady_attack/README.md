# SM3 生日攻击

通过生日攻击来构造 SM3 哈希结果前n-bit相同的碰撞。其中SM3 通过python的实现参考博客(https://blog.csdn.net/qq_37726361/article/details/84196058)。然后构造一个列表来存放随机元素哈希结果的前n位，若该列表内有重复元素代表存在碰撞。

运行结果如下：
![image](https://github.com/lumingfeifei0/homework-for-security/blob/main/sm3_birthady_attack/capture_20220729160613978.jpg)

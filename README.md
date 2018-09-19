Gomoku

Chươnng trình game caro sử dụng  Turtle trong python và engine AI dựa trên thuật toán minimax, cắt tỉa alpha-beta cùng với heuristic điểm số 4 hướng.

**Thuật toán**

1.Thuật toán Minimax

- Minimax là một thuật toán đệ quy lựa chọn bước đi kế tiếp trong một trò chơi 2 người bằng cách tính các giá trị cho các Node trên cây trò chơi sau đó tìm Node có giá trị phù hợp để đi bước tiếp theo.

- Hai đối thủ trong trò chơi được gọi là MIN và MAX luân phiên thay thế nhau đi. MAX đại diện cho người quyết dành thắng lợi và cố gắng tối đa hóa ưu thế của mình, ngược lại người chơi đại diện cho MIN lại cố gắng giảm điểm số của MAX và cố gắng làm cho điểm số của mình càng âm càng tốt. Giả thiết đưa ra MIN và MAX có kiến thức như nhau về không gian trạng thái trò chơi và cả hai đối thủ đều cố gắng như nhau.
Mỗi Node biểu diễn cho một trạng thái trên cây trò chơi. Node lá là Node chứa trạng thái kết thúc của trò chơi.

Giải thuật Minimax thể hiện bằng cách định trị các Node trên cây trò chơi:

+ Node thuộc lớp MAX thì gán cho nó giá trị lớn nhất của con Node đó.
+ Node thuộc lớp MIN thì gán cho nó giá trị nhỏ nhất của con Node đó.
Từ các giá trị này người chơi sẽ lựa chọn cho mình nước đi tiếp theo hợp lý nhất.
- Nếu như đạt đến giới hạn tìm kiếm (đến tầng dưới cùng của cây tìm kiếm tức là trạng thái kết thúc của trò chơi).
- Tính giá trị của thế cờ hiện tại ứng với người chơi ở đó. Ghi nhớ kết quả.
- Nếu như mức đang xét là của người chơi cực tiểu (nút MIN), áp dụng thủ tục Minimax này cho các con của nó. Ghi nhớ kết quả nhỏ nhất.
- Nếu như mức đang xét là của người chơi cực đại (nút MAX), áp dụng thủ tục Minimax này cho các con của nó. Ghi nhớ kết quả lớn nhất.
2. Thuật toán cắt tỉa alpha-beta.

- Vì sự bùng nổ cây trò chơi trong minimax nên ta sẽ bỏ những nút không tối ưu bằng cách cắt tỉa alpha-beta.

- Tư tưởng: + Nếu một nhánh tìm kiếm nào đó không th? cải thiện ??i với giá trị mà chúng ta đã có, thì không cần xét đến hàm đó n?a -> tiết kiệm chi phí thời gian, bộ nhờ cho cây tìm ki?m
		 + Dùng hai c?n Anpha và Beta ?? so sánh và lo?i b? các tr??ng h?p s? không c?n xét ??n trong thu?t toán minimax.	

- Mô t?: + Anpha lưu nướcc đi tốt nhất của máy, Beta lưu giá trị tốt nhất của Người chơi
	   + Nếu bất cứ khi nào anpha >= beta, thì người chơi chắc chắn sẽ chọn nước đi tốt nhất cho họ và cưỡng bức nước đi tồi hơn anpha cho máy, vì vậy mà không cần xét thêm bước nào nữa.


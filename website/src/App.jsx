import React, { useState } from "react";

const PRODUCTS = [
  {
    id: "capcut",
    name: "CapCut Pro",
    price: 25000,
    file: "capcut.txt",
  },
  {
    id: "chatgpt",
    name: "ChatGPT Plus",
    price: 80000,
    file: "chatgpt.txt",
  },
  {
    id: "canva",
    name: "Canva Pro",
    price: 30000,
    file: "canva.txt",
  },
];

function ProductCard({ product, stock, onBuy }) {
  return (
    <div style={{ border: '1px solid #ccc', padding: 16, margin: 8, borderRadius: 12 }}>
      <h2>{product.name}</h2>
      <p>Giá: {product.price.toLocaleString()}đ</p>
      <p>Còn lại: {stock} tài khoản</p>
      <button onClick={() => onBuy(product)} disabled={stock <= 0}>
        Mua ngay
      </button>
    </div>
  );
}

export default function App() {
  const [selected, setSelected] = useState(null);
  const [step, setStep] = useState(1);
  const [orderId, setOrderId] = useState("");

  const generateOrderId = () => {
    return "QUOC-" + Math.floor(100000 + Math.random() * 900000);
  };

  const handleBuy = (product) => {
    const id = generateOrderId();
    setOrderId(id);
    setSelected(product);
    setStep(2);
  };

  const getStock = (fileName) => {
    const mockStock = {
      "capcut.txt": 12,
      "chatgpt.txt": 4,
      "canva.txt": 20,
    };
    return mockStock[fileName] || 0;
  };

  if (step === 2 && selected) {
    return (
      <div style={{ padding: 20 }}>
        <h1>Thông tin đơn hàng</h1>
        <p>Sản phẩm: {selected.name}</p>
        <p>Giá: {selected.price.toLocaleString()}đ</p>
        <p style={{ fontWeight: "bold" }}>Mã đơn hàng: {orderId}</p>
        <p>Chuyển khoản đến:</p>
        <p><b>Ngân hàng:</b> MB Bank</p>
        <p><b>Số tài khoản:</b> 00500920098386</p>
        <p><b>Chủ tài khoản:</b> Le Minh Quoc</p>
        <p><b>Nội dung chuyển khoản:</b> {orderId}</p>
        <p>Sau khi chuyển khoản, hệ thống sẽ tự động giao tài khoản.</p>
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Shop Bán Tài Khoản Tự Động</h1>
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {PRODUCTS.map((product) => (
          <ProductCard
            key={product.id}
            product={product}
            stock={getStock(product.file)}
            onBuy={handleBuy}
          />
        ))}
      </div>
    </div>
  );
}

